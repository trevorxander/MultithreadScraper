import scraper
from scraper import UrlList
import threading
import time



if __name__ == "__main__":



    driver = 'drivers/chromedriver'


    conc_threads = 30
    scraping_threads = []

    start_time = time.time()
    no_of_urls = 5

    url_queue = UrlList("dataset/dead_url.txt")

    for url in url_queue:
        print(url)


    for url in range(0, no_of_urls):

        while threading.active_count() > conc_threads:
            time.sleep(0)
        #thread = scraper.ScraperThread(driver, url_queue.next_url)
        #thread.start()

        #scraping_threads.append(thread)

    while threading.active_count() > 1:
        for thread in threading.enumerate():
            try:
              thread.join()
            except:
                continue

    dead_urls = set(open('dataset/dead_url.txt','r').readlines())





    end_time = time.time()

    print((end_time - start_time)/no_of_urls, 's per url')



