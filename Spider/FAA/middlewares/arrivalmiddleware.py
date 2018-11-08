from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from scrapy.http import HtmlResponse
import time

class ArrivalDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    # def __init__(self):
    #     download_path = os.path.join(os.path.abspath('.'), 'download')
    #     profile = webdriver.FirefoxProfile()
    #     profile.set_preference('browser.download.dir', download_path)
    #     profile.set_preference('browser.download.folderList', 2)
    #     profile.set_preference('browser.download.manager.showWhenStarting', False)
    #     # Even though we are going to download .csv file, the 'Content-Type' we see from the Response is 'application/text'
    #     profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/text')
    #     self.browser = webdriver.Firefox(firefox_profile=profile)
    #     self.browser.implicitly_wait(60)


    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if spider.start_flag == 0:
            return None
        elif spider.start_flag == 1:
            spider.browser.get(spider.url)
            airport = request.meta.get('airport')
            airline = request.meta.get('airline')
            spider.log('[*] Crawling Airport=%s, Airline=%s' % (airport, airline))
            # wait until 'submit' button is presented
            element = WebDriverWait(spider.browser, 15).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
            # Statistics (checkbox)
            element = spider.browser.find_element_by_xpath("//input[@id='chkAllStatistics']")
            if not element.is_selected():
                element.click()
            # Origin Airport (dropdown)
            element = spider.browser.find_element_by_xpath("//select[@id='cboAirport']//option[@value=\'%s\']" % airport)
            element.click()
            # Airline (dropdown)
            element = spider.browser.find_element_by_xpath("//select[@id='cboAirline']//option[@value=\'%s\']" % airline)
            element.click()
            # Months (checkbox)
            if spider.config['months'][0].upper() == 'ALL':
                element = spider.browser.find_element_by_xpath("//input[@id='chkAllMonths']")       # All months
                if not element.is_selected():
                    element.click()
            else:
                for month in spider.config['months']:
                    element = spider.browser.find_element_by_xpath("//input[@id='chkMonths_%s']" % (int(month)-1))  # Certain month (Start from 0)
                    if not element.is_selected():
                        element.click()
            # Days (checkbox)
            if spider.config['days'][0].upper() == 'ALL':
                element = spider.browser.find_element_by_xpath("//input[@id='chkAllDays']")         # All days
                if not element.is_selected():
                    element.click()
            else:
                for day in spider.config['days']:
                    element = spider.browser.find_element_by_xpath("//input[@id='chkDays_%s']" % (int(day)-1))      # Certain day (Start from 0)
                    if not element.is_selected():
                        element.click()
            # Years (checkbox)
            if spider.config['years'][0].upper() == 'ALL':
                element = spider.browser.find_element_by_xpath("//input[@id='chkAllYears']")        # All days
                if not element.is_selected():
                    element.click()
            else:
                for year in spider.config['years']:
                    element = spider.browser.find_element_by_xpath("//input[@id='chkYears_%s']" % (int(year)-1987)) # Certain year (1987->0)
                    if not element.is_selected():
                        element.click()
            # Submit
            element = spider.browser.find_element_by_xpath("//input[@id='btnSubmit']")
            element.click()
            # wait until 'submit' button is presented
            element = WebDriverWait(spider.browser, 15).until(EC.presence_of_element_located((By.ID, "lblAirport")))
            # Download CSV
            try:
                element = spider.browser.find_element_by_xpath("//a[@id='DL_CSV']")
                element.click()
                time.sleep(6)       # wait for the downloading. will modify it to a more smart method
                spider.log('[*] Download information successfully: airport=%s, airline=%s' % (airport, airline))
            except exceptions.NoSuchElementException as e:
                spider.log('[*] No information is crawled @airport=%s, airline=%s' % (airport, airline))
                raise
            # return None
            finally:
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
