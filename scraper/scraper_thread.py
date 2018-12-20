import threading
import time
from selenium import webdriver
from selenium import common
from threading import Lock
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from scraper.scraper_data import PageData
from scraper.scraper_data import PageDataCollection

class ScraperThread (threading.Thread):
    data_collection = PageDataCollection("dataset/page_data.txt")
    threadLock = Lock()
    def __init__(self, driver_location, url):
        threading.Thread.__init__(self)
        self.driver_loc = driver_location
        self.url = url
        self.data = PageData()

    def run(self):
        try:
            self.scraper = SearchScraper(self.driver_loc, self.url)
            self.data.add_data("url", [self.url])
            self.data.add_data('title', [self.scraper.get_title()])

            self.data.add_data('description',self.scraper.get_description())
            self.data.add_data('words', self.scraper.get_keywords())

            sub_domains = self.scraper.get_links()
            for url in sub_domains:
                thread = ScraperThread(self.driver_loc, url)
            self.data.add_data('links', sub_domains)

            ScraperThread.threadLock.acquire()
            ScraperThread.data_collection.add_page(self.data)
            ScraperThread.threadLock.release()


        except common.exceptions.TimeoutException:
            print('Error:'  + self.url + ' timed out')
        except common.exceptions.StaleElementReferenceException:
            print('Error: Could not partse HTML for ' + self.url)
        finally:
            self.scraper.driver.close()
            return

class SearchScraper:
    def __init__(self, driver_location, url):

        chrom_options = Options()
        prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                            'notifications': 2, 'auto_select_certificate': 2,
                                                            'fullscreen': 2, 'disk-cache-size': 4096,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2,
                                                            'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2,
                                                            'site_engagement': 2,
                                                            'durable_storage': 2}}
        chrom_options.add_experimental_option("prefs", prefs)
        chrom_options.add_argument('--headless')
        chrom_options.Proxy = None
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "normal"
        self.driver = webdriver.Chrome(driver_location, desired_capabilities=capa, chrome_options=chrom_options)

        self._open_page(url)



    def _open_page(self, url):
        self.driver.implicitly_wait(10)
        if url.startswith('http') or url.startswith('https'):
            self.url = url
            self.driver.get(url)
        else:
            try:
                self.driver.get('https://' + url)
                self.url = 'https://' + url
            except:
                self.__init__(self.driver, 'http://' + url)
                self.url = 'http://' + url

    def get_keywords (self):
        page = self.driver.find_element_by_tag_name("html").text
        page = page.split()
        object = {}
       # for word in page_content:
            # if there's a non-character ignore the word  (^[a-zA-Z]+)
            # STORE IT INTO AN OBJECT SO I CAN DO getUrlPriority and then we can store into database
        # getUrlPriority
        return page

    def get_links(self):
        links = self.driver.find_elements_by_tag_name('a')
        link_list = []
        for sub_domain in links:
            link_list.append(sub_domain.get_attribute("href"))

        return (link_list)

    def get_title(self):
        title = self.driver.title
        return title

    def get_category(self):
        meta = self.driver.find_element_by_tag_name("meta")
        print(meta)

    def get_description (self):
        getElem = [(self.driver.find_element_by_name, ('description')),
                   (self.driver.find_element_by_name, ('Description'))]

        description = None
        for (func, param) in getElem:
            try:
                description = func(param).get_attribute('content')
            except common.exceptions.NoSuchElementException:
                continue
            except common.exceptions.StaleElementReferenceException:
                continue

        if description is None:
            description = "null"
        return [description]



