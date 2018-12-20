import scraper
from scraper import UrlList
import threading
import time

if __name__ == "__main__":

    driver = 'drivers/chromedriver'


    conc_threads = 30
    scraping_threads = []

    start_time = time.time()
    max_urls = 9999999

    url_queue = UrlList("dataset/top_websites.txt")

    url_count: int
    for url_count,url in enumerate(url_queue):
        if url_count > max_urls:
            break
        while threading.active_count() > conc_threads:
            time.sleep(0)
        thread = scraper.ScraperThread(driver, url)
        thread.start()
        scraping_threads.append(thread)

    while threading.active_count() > 1:
        for thread in threading.enumerate():
            try:
              thread.join()
            except:
                continue

    scraper.ScraperThread.data_collection.flush()

    end_time = time.time()

    print((end_time - start_time) / url_count, 's per url')



