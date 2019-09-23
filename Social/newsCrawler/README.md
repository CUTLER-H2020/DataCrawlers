# Documentation

## Requirements
1. Installation of the Mozilla Geckodriver is needed for the Selenium Middleware to run.

Current releases can be found [here](https://github.com/mozilla/geckodriver/releases) and additional information on Selenium [here](https://selenium-python.readthedocs.io/installation.html).

Alternatively, a different driver supported by Selenium could be used. This would require changes in the custom_settings of the NewsSpider class in newsspider.py.

2. An API key for [News API](https://newsapi.org/) has to be specified in a .env file of the directory under the keyname "NEWS_API_KEY"

## Usage

1. ./news_crawler.py KEYWORD START_DATE END_DATE retrieves comments from news articles for the given keyword(s) and the given timeframe.

Keywords can be matched as exact phrases by surrounding them with parentheses. They can also be concatenated with AND or OR, e.g. "parking AND space"-

A documentation of the Keywords is found [here](https://newsapi.org/docs/endpoints/everything)

The retrieved comments are currently stored in a file.

2. ./news_es.py FILENAME

This file is given to the ElasticSearch wrapper in order to index the documents in the specific ElasticSearch index.

## Useful ressources

1. [News API Documentation](https://newsapi.org/docs/)

2. [Scrapy Documentation](https://docs.scrapy.org/en/latest/)

3. [Selenium Documentation, inluding installation manual](https://selenium-python.readthedocs.io/)

4. The index mapping for news comments is found under CUTLER-dev/es-configs/mappings/cutler_news

5. [Documentation for the used topic model](https://github.com/ckling/promoss)
