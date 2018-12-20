import threading
import time
from selenium import webdriver
from selenium import common
from threading import Lock
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import NewType

class ScraperThread (threading.Thread):
    threadLock = Lock()
    def __init__(self, driver_location, url):
        self.driver_loc = driver_location
        self.url = url
        threading.Thread.__init__(self)



    def run(self):

        self.scraper = SearchScraper(self.driver_loc, self.url)
        description = self.scraper.get_description()
        self.scraper.get_keywords()
        #print(self.scraper.get_links())
        #print(self.scraper.get_category())
        self.scraper.driver.close()



        if (description == None):
            ScraperThread.threadLock.acquire(True)
            self.file.write(self.url)
            ScraperThread.threadLock.release()
        # links = self.scraper.get_links()

        # for sub_domain in links:
        #    thread = ScraperThread(self.driver_loc, sub_domain)
        #    thread.start()
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
        print(url)
        self.driver.implicitly_wait(10)
        try:
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
        except:
            print ('website timed out')

    def get_keywords (self):
        page: str
        page = self.driver.find_element_by_tag_name("html").text
        page_content = page.split()
        print(len(page_content))
        object = {}
        for word in page_content:
            # if there's a non-character ignore the word  (^[a-zA-Z]+)
            # STORE IT INTO AN OBJECT SO I CAN DO getUrlPriority and then we can store into database
            print('test')
        # getUrlPriority
        return page

    def get_links(self):
        elems = self.driver.find_elements_by_tag_name("a")
        for elem in elems:
            print (elem.get_attribute("href"))

    def get_title(self):
        title = self.driver.title
        return title

    def get_category(self):
        meta = page = self.driver.find_element_by_tag_name("meta")
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

        return description


    def get_URL_priority (self, word):

        print('test')


