from multithread_scraper import scraper_data
from multithread_scraper import scraper
import sys
import time
import threading
from threading import Lock


class MultithreadScraper:

    _MAX_URLS = int(sys.maxsize)
    _DRIVER_LOC = '../drivers/chromedriver'
    _INPUT_FILE = '../data/top_websites.txt'
    _OUTPUT_FILE = '../data/page_data.txt'

    def __init__(self, max_threads=5):

        scraping_threads = []
        start_time = time.time()

        url_queue = scraper_data.UrlList(MultithreadScraper._INPUT_FILE)

        max_active_thread = threading.active_count() + max_threads
        url_count: int
        for url_count, url in enumerate(url_queue):
            if url_count > MultithreadScraper._MAX_URLS - 1:
                break
            while threading.active_count() > max_active_thread:
                time.sleep(0)
            thread = ScraperThread(MultithreadScraper._DRIVER_LOC, url)
            thread.start()
            scraping_threads.append(thread)

        while threading.active_count() > 1:
            for thread in threading.enumerate():
                try:
                    thread.join()
                except:
                    continue

        ScraperThread.data_collection.flush()

        end_time = time.time()

        print((end_time - start_time) / url_count, 's per url')


class ScraperThread(threading.Thread):
    data_collection = scraper_data.PageDataCollection(MultithreadScraper._OUTPUT_FILE)
    threadLock = Lock()

    def __init__(self, driver_location, url):
        threading.Thread.__init__(self)
        self.driver_loc = driver_location
        self.url = url
        self.data = scraper_data.PageData()

    def run(self):
        self.scraper = scraper.SearchScraper(self.driver_loc, self.url)

        page_data = self.scraper.scrape_all()
        sub_domains = page_data.get_data('URL')

        ScraperThread.threadLock.acquire()
        try:
            ScraperThread.data_collection.add_page(page_data)
        finally:
            ScraperThread.threadLock.release()
