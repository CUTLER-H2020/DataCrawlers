from scrapy.crawler import CrawlerProcess
from newsspider import *


class Process:
    """
    This class servers as a wrapper for a Scrapy CrawlerProcess
    """

    def start(self, urls):
        """
        Starts a crawlerprocess with the NewsSpider and the urls, which are to be crawled
        as arguments
        :param urls: list List of urls to be crawled
        """
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(NewsSpider, start_urls=urls)
        process.start()