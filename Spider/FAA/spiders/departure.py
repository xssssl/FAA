import scrapy
from selenium import webdriver
from .parseconfig import Parsedeparture
import os
from scrapy import signals

class DepartureSpider(scrapy.Spider):
    name = "departure"

    def __init__(self):
        super(DepartureSpider, self).__init__()
        self.url = 'https://www.transtats.bts.gov/ONTIME/Departures.aspx'
        download_path = os.path.join(os.path.abspath('.'), 'download')
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('browser.download.dir', download_path)
        self.profile.set_preference('browser.download.folderList', 2)
        self.profile.set_preference('browser.download.manager.showWhenStarting', False)
        # Even though we are going to download .csv file, the 'Content-Type' we see from the Response is 'application/text'
        self.profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/text')
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        self.browser = webdriver.Firefox(firefox_options=firefox_options, firefox_profile=self.profile)
        self.browser.implicitly_wait(15)
        self.config = Parsedeparture().readall()
        self.start_flag = 0

    # close the browser when the spider is closed
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DepartureSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.getinfo)

    # Get Airlines and Origin Airports information
    def getinfo(self, response):
        airlines = response.xpath("//select[@id='cboAirline']//option/@value").extract()
        if len(airlines):
            self.log('[*] Get airlines list: %s' % airlines)
        else:
            self.log('[!] Failed to get airlines information')
            raise ValueError
        airports = response.xpath("//select[@id='cboAirport']//option/@value").extract()
        if len(airports):
            self.log('[*] Get airports list: %s' % airports)
        else:
            self.log('[!] Failed to get airlines information')
            raise ValueError

        self.start_flag = 1     # indicate that it's time to start crawling
        # self.browser.get(self.url)
        for airport in self.config['origin_airports']:
            if airport not in airports:
                self.log('[!] Airport name error: %s' % airport)
            else:
                if self.config['airlines'][0].upper() == 'ALL':
                    for airline in airlines:
                        # dont_filter is used to crawl duplicated url
                        yield scrapy.Request(url=self.url, callback=self.parse, meta={'airline': airline, 'airport': airport}, dont_filter=True)
                else:
                    for airline in self.config['airlines']:
                        if airline in airlines:
                            yield scrapy.Request(url=self.url, callback=self.parse,
                                                 meta={'airline': airline, 'airport': airport}, dont_filter=True)
                        else:
                            self.log('[!] Airline name error: %s' % airline)


    def parse(self, response):
        pass

    def spider_close(self, spider):
        self.log('[*] All the tasks have been done. Spider is going to be closed.')
        self.browser.quit()

