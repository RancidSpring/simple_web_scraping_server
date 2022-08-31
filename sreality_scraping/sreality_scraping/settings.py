BOT_NAME = 'sreality_scraping'

SPIDER_MODULES = ['sreality_scraping.spiders']
NEWSPIDER_MODULE = 'sreality_scraping.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = "/driver/chromedriver"
SELENIUM_DRIVER_ARGUMENTS = ['--no-sandbox', '--headless', '--disable-dev-shm-usage']

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

# LOG_LEVEL = 'DEBUG'  # to only display errors
# LOG_FORMAT = '%(levelname)s: %(message)s'
# LOG_FILE = 'log.txt'