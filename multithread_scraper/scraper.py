import re
from selenium import webdriver
from selenium import common
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


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
        chrom_options.add_argument('--no-sandbox')
        chrom_options.Proxy = None
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "normal"
        self._driver = webdriver.Chrome(driver_location, desired_capabilities=capa, chrome_options=chrom_options)
        self._url = url

        self._scraper_functions = [self.get_title,
                                   self.get_url,
                                   self.get_description,
                                   self.get_keywords,
                                   # self.get_category,
                                   self.get_links]

        self._open_page()

    def quit(self):
        self._driver.close()
        self._driver.quit()

    def _open_page(self):
        self._driver.implicitly_wait(5)
        if self._url.startswith('http') or self._url.startswith('https'):
            self._driver.get(self._url)
            return
        else:
            try:
                self._driver.get('https://' + self._url)
                self._url = 'https://' + self._url
            except:
                self.__init__(self._driver, 'http://' + self._url)
                self._url = 'http://' + self._url

    def scrape_all(self):
        website_data = {}
        try:
            for website_data_funcs in self._scraper_functions:
                data_piece = website_data_funcs()
                type_of_data = data_piece[0]
                data = data_piece[1]
                website_data[type_of_data] = data
        except common.exceptions.StaleElementReferenceException:
            print('Stale element ')
        except common.exceptions.NoSuchElementException:
            print('Could not find element')
        except common.exceptions.WebDriverException:
            print('Unknown error')

        return website_data

    def get_keywords(self):
        all_words = self._driver.find_element_by_tag_name("html").text
        all_words = all_words.split()
        key_words = []
        for word in all_words:
            if re.fullmatch('^[a-zA-z]+', word) is not None:
                key_words.append(word)
        return 'Words', key_words

    def get_links(self):
        links = self._driver.find_elements_by_tag_name('a')
        link_list = []

        for sub_domain in links:
            link = sub_domain.get_attribute("href")
            if link is not None:
                # Add validation to check if url is a subdomain
                link_list.append(link)

        return 'Subdomains', link_list

    def get_title(self):
        title = self._driver.title
        return 'Title', [title]

    def get_category(self):
        meta = self._driver.find_element_by_tag_name("meta")
        return 'Category', [meta]

    def get_description(self):
        getElem = [(self._driver.find_element_by_name, ('description')),
                   (self._driver.find_element_by_name, ('Description'))]

        description = None
        for (func, param) in getElem:
            try:
                description = func(param).get_attribute('content')  # bottleneck
            except common.exceptions.NoSuchElementException:
                continue
            except common.exceptions.StaleElementReferenceException:
                continue

        if description is None:
            description = "null"
        return 'Description', [description]

    def get_url(self):
        return 'URL', [self._url]
