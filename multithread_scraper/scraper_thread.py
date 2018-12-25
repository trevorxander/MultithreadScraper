from multithread_scraper import scraper_data
from multithread_scraper import scraper

import sys
import time
import threading
from threading import Lock


class MultithreadScraper:
    _MAX_URLS = int(sys.maxsize)

    def __init__(self, max_threads=None,
                 input=None,
                 output=None,
                 driver=None):

        scraping_threads = []
        start_time = time.time()

        url_queue = scraper_data.UrlList(input)

        max_active_thread = threading.active_count() + max_threads
        url_count: int
        for url_count, url in enumerate(url_queue):
            if url_count > MultithreadScraper._MAX_URLS - 1:
                break
            while threading.active_count() > max_active_thread:
                time.sleep(0)
            thread = ScraperThread(driver, url, output)
            thread.start()
            scraping_threads.append(thread)

        for thread in scraping_threads:
            try:
                thread.join()
            except:
                continue

        ScraperThread.page_data_buffer.flush()

        end_time = time.time()

        print((end_time - start_time) / url_count, 's per url')


class ScraperThread(threading.Thread):
    page_data_buffer: scraper_data.PageDataCollection
    _first_call = True
    _threadLock = Lock()

    def __init__(self, driver_location, url_to_scrape, out_file):
        threading.Thread.__init__(self)
        self.driver_loc = driver_location
        self.url = url_to_scrape

        ScraperThread._threadLock.acquire()
        try:
            if ScraperThread._first_call:
                ScraperThread.page_data_buffer = scraper_data.PageDataCollection(out_file)
                ScraperThread._first_call = False
        finally:
            ScraperThread._threadLock.release()

    def run(self):
        search_scraper = scraper.SearchScraper(self.driver_loc, self.url)
        page_data = search_scraper.scrape_all()
        search_scraper.quit()
        sub_domains = page_data['Subdomains']
        ScraperThread.page_data_buffer.add_page(page_data)
        return
