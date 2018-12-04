# settings needed for scrapy-splash, following the docs at:
# https://github.com/scrapy-plugins/scrapy-splash
# usage: docker run -p 8050:8050 scrapinghub/splash
from shutil import which

#SPLASH_URL = 'http://localhost:8050'

SELENIUM_DRIVER_NAME='firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH=which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless']

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}