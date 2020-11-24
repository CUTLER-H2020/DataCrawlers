import pandas as pd
from pre_process_funcs import *


def get_and_write_corpus(df_comments):
    """
    Transforms the input data into the structure required by the Promoss package, writes it into a corpus.txt file and
    returns the complete data as a pandas.DataFrame.
    See https://github.com/ckling/promoss for more info.

    :param df_comments: The location of the file containing the comments.

    :return: pandas.DataFrame Containing the complete comment data
    """
    processed_comments = get_preprocessed_texts(df_comments)

    df_comments['processed'] = processed_comments
    to_txt(processed_comments)
    return df_comments


def get_preprocessed_texts(df):
    """
    Returns a series with the pre processed documents.

    :param location: Location of the file, which contains the data for the pandas.DataFrame.
    :return:         pandas.Series with the pre processed documents.
    """
    return df.comment.map(pre_process)


def to_txt(series):
    """
    Writes the series to a txt file as required for the Promoss package.
    See https://github.com/ckling/promoss for mor info.

    :param series: The series, which is to be written into a file.a
    :return:
    """
    return series.to_csv('corpus.txt', sep='\n', index=False)


if __name__ == '__main__':
    pass
