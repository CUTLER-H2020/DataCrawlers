import scrapy
import json
import csv
import re
import warnings
from scrapy_selenium.http import SeleniumRequest
from shutil import which
from bs4 import BeautifulSoup
from comment_classifier import *

class NewsSpider(scrapy.Spider):
    """
    This class is responsible for the actual crawling and news article comment retrieval
    """

    name = "newsspider"

    custom_settings = {
        'SELENIUM_DRIVER_NAME' : 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH' : which('geckodriver'),
        'SELENIUM_DRIVER_ARGUMENTS' : ['--headless'],
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy_selenium.middleware.SeleniumMiddleware': 800
    },
    }


    def __init__(self, start_urls=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls

    def start_requests(self):
        """
        Starts the requests with the urls of the spider
        """
        for url in self.start_urls:
            body = json.dumps({"url": url, "wait": 0.5, "js_enabled": True})
            headers = scrapy.http.headers.Headers({'Content-Type': 'application/json'})
            yield SeleniumRequest(callback=self.parse, url=url)

    def parse(self, response):
        """
        parses the crawled urls and retrieves comments from the comment section of the
        news article in the url, if such comments exist
        :param response:
        """
        # filters url warnings given by BeautifulSoup
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

        #load load classifier and word features
        comment_clf = CommentClassifier('comment_clf.pkl', 'word_features.pkl')
        # retrieve comment area
        raw_comment_area = response.xpath("//div[contains(@class, 'comment') or contains(@id, 'comment')]//text()").extract()

        #this is sufficient to filter out some javascript and CSS
        regexp = re.compile('function((.+))|{(.+);(.+)}')

        # filter out comments from the comment area
        with open('comments.csv', 'a') as f:
            csvWriter = csv.writer(f)
            i=0
            for token in set(raw_comment_area):
                # this solves a shortcoming of the xpath extraction, where html or javascript code is falsely extracted as text
                if not bool(BeautifulSoup(token, "html.parser").find()) and not regexp.search(token):
                    # threshold might be reevaluated
                    processed_c = [comment_clf.get_features(comment_clf.pre_process(token), comment_clf.word_features)]
                    if comment_clf.clf.predict_proba(processed_c)[0][1] > 0.25:
                        csvWriter.writerow([i, token])
                        i += 1

        iframes = response.xpath("//iframe[starts-with(@src, 'http://disqus.com') or "
                                 "starts-with(@src, 'https://disqus.com') or contains(@src, 'spot.im')]"
                                 "/@src").extract()
        for iframe in iframes:
            yield SeleniumRequest(callback=self.parseFrame, url=iframe)

    def parseFrame(self, response):
        """
        This function is responsible for crawling disQus and spot.im iFrames, which need a special treatment,
        as they have to be loaded separately from the page
        :param response:
        """
        filename = 'comments.csv'
        comments_disqus = response.xpath("//div[contains(@class, 'post-message')]//p//text()").extract()
        comments_spot = response.xpath("//div[contains(@class, 'sppre_entity sppre_text-entity')]//text()").extract()

        with open(filename, 'a',  newline='') as f:
            csvWriter = csv.writer(f)
            for index, comment in enumerate(comments_disqus+comments_spot):
                csvWriter.writerow([index, comment])