import nltk
from nltk.corpus import stopwords
from itertools import permutations

def extract_terms(term):
    # Used when tokenizing words
    sentence_re = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
        '''

    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()

    #Taken from Su Nam Kim Paper...
    grammar = r"""
        NBAR:
            {<JJ>*<NN.*>*}      # Adjectives, terminated with Nouns
        VNP:
            {<VBP><NBAR>}       # Verb + Noun
        NP:
            {<VNP>}
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)

    toks = nltk.regexp_tokenize(term, sentence_re)
    postoks = nltk.tag.pos_tag(toks)

    #print(postoks)

    tree = chunker.parse(postoks)

    stopwords_en = stopwords.words('english')

    terms = get_terms(tree, stopwords_en, stemmer, lemmatizer)
    terms = [ ' '.join(term) for term in terms if len(term) > 1 ]

    return terms

def get_trigram(text, trigram_raw):
    # Used when tokenizing words
    sentence_re = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
        '''

    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()

    #Taken from Su Nam Kim Paper...
    grammar = r"""
        NBAR:
            {<JJ>*<NN.*>*}      # Adjectives, terminated with Nouns
        VNP:
            {<VBP><NBAR>}       # Verb + Noun
        NP:
            {<VNP>}
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)

    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)

    #print(postoks)

    tree = chunker.parse(postoks)

    stopwords_en = stopwords.words('english')

    terms = get_terms(tree, stopwords_en, stemmer, lemmatizer)
    terms = [term for term in terms]

    word1, word2, word3 = trigram_raw.split(' ')

    for trial in permutations([word1, word2, word3]):
        if list(trial) in terms:
            # found plausible trigram
            return ' '.join(trial)

    return trigram_raw

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word, stemmer, lemmatizer):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word, stopwords_en):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
                    and word.lower() not in stopwords_en)
    return accepted


def get_terms(tree, stopwords_en, stemmer, lemmatizer):
    for leaf in leaves(tree):
        term = [ normalise(w, stemmer, lemmatizer) for w,t in leaf if acceptable_word(w, stopwords_en) ]
        yield term


