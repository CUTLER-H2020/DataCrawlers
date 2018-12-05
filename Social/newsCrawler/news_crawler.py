import json
import dateutil.parser
from news_process import *
from news_auth import *
import requests
import sys
import urllib
import datetime
from math import ceil
from multiprocessing import Pool, current_process


class NewsCrawler:
    """
    A class for the retrieval of news article comments
    It is possible to query for news article comments by keyword and a timeframe

    example usage:
    $ python3 news_crawler.py "some keyword(s)" 2018-01-01 2018-01-01

    Powered by News API https://newsapi.org
    """

    def __init__(self):
        self.auth = NewsAuth()

    def get_no_of_pages(self, keyword, since=None, to=None):
        """
        Returns the number of request pages available for the given keyword in the
        given timeframe
        :param keyword: String the keyword to look for
        :param since: String start of the timeframe, has to be isoformattable
        :param to: String end of the timeframe, has to be isoformattable
        :return: Int
        """
        response = self.get_news(keyword, since, to)
        total_results = json.loads(response)['totalResults']
        return 1 if total_results/20 == 0 else ceil(total_results/20)

    def get_news(self, keyword, since=None, to=None, page=None):
        """
        Returns the newsapi query result
        :param keyword: String the keyword to look for
        :param since: String start of the timeframe, has to be isoformattable
        :param to: String end of the timeframe, has to be isoformattable
        :param page: Int the page to query
        :return: Bytes
        """
        payload = {}
        url = "https://newsapi.org/v2/everything"
        payload['q'] = keyword
        if since is not None:
            try:
                start_dt = dateutil.parser.parse(since)
                if to is not None:
                    to_dt = dateutil.parser.parse(to)
                else:
                    to_dt = datetime.datetime.now()
            except ValueError:
                raise IOError('since parameter can not be converted to datetime')
            payload['from'] = start_dt.isoformat()
            payload['to'] = to_dt.isoformat()
            payload['language'] = 'en'
            payload['pageSize'] = 20
            payload['sortBy'] = 'popularity'
            payload['excludeDomains'] = 'startribune.com'
            if page is not None and type(page) == int and page > 0:
                payload['page'] = page
        r = requests.get(url, auth=self.auth, params=payload)
        return r.content

    def crawl(self, keyword, since=None, to=None):
        """
        This function deals with the entire crawling process
        It distributes the different pages on worker processes, which crawl the given
        page for news article comments
        :param keyword: String the keyword to look for
        :param since: String start of the timeframe, has to be isoformattable
        :param to: String end of the timeframe, has to be isoformattable
        """
        no_of_pages = self.get_no_of_pages(keyword, since, to)
        print('pages: ' + str(no_of_pages))
        self.keyword = keyword
        self.since = since
        self.to = to
        p = Pool()
        p.map(self.distribute, range(1, no_of_pages+1))

    def crawl_page(self, keyword, since=None, to=None, page=None):
        """
        Crawls a certain page of the given keyword and given timeframe
        :param keyword: String the keyword to look for
        :param since: String start of the timeframe, has to be isoformattable
        :param to: String end of the timeframe, has to be isoformattable
        :param page: Int the page to query
        """
        data = self.get_news(keyword, since, to, page)
        print(current_process())
        print('crawling page no.: ' + str(page))
        urls = self.get_urls(data)
        p = Process()
        p.start(urls)

    def distribute(self, page):
        """
        Distributes the different pages to worker processes
        :param page: Int the page to query
        """
        self.crawl_page(self.keyword, self.since, self.to, page)

    def get_urls(self, data):
        """
        Retrieves the urls from the newsapi response
        :param data: The entire response content
        :return: list
        """
        data = json.loads(data)
        urls = []
        for article in data['articles']:
            urls.append(article['url'])
        return urls


if __name__ == '__main__':
    if len(sys.argv) not in (3,4):
        raise IOError('Number of arguments is faulty')
    keyword = sys.argv[1]
    since = sys.argv[2]
    nc = NewsCrawler()
    nc.keyword = sys.argv[1]
    nc.since = sys.argv[2]
    if len(sys.argv) is 4:
        to = sys.argv[3]
        nc.to = sys.argv[3]
        nc.crawl(keyword, since=since, to=to)
    else:
        nc.crawl(keyword, since=since)