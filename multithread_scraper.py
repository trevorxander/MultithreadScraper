import scraper
import threading
import thread
import time



def load_file():


    file = open('dataset/url_list.txt','r')
    return file.readlines()

if __name__ == "__main__":


    driver = 'drivers/chromedriver'
    url_list = load_file()

    conc_threads = 10
    scraping_threads = []

    for url in url_list:
        while threading.active_count() > conc_threads:
            time.sleep(0)
        thread = scraper.ScraperThread (driver, url)
        thread.start()
        scraping_threads.append(thread)

    for thread in scraping_threads:
        thread.join()





