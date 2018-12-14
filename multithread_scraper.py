import scraper
import threading
import time



def load_file():


    file = open('dataset/url_list.txt','r')
    return file.readlines()

if __name__ == "__main__":

    driver = 'drivers/chromedriver'
    url_list = load_file()

    conc_threads = 30
    scraping_threads = []

    start_time = time.time()
    no_of_urls = 20
    for url in range(0, no_of_urls):
        while threading.active_count() > conc_threads:
            time.sleep(0)
        thread = scraper.ScraperThread(driver, url_list[url])
        thread.start()

        scraping_threads.append(thread)

    while threading.active_count() > 1:
        for thread in threading.enumerate():
            try:
              thread.join()
            except:
                continue




    dead_urls = set(open('dataset/dead_url.txt','r').readlines())





    end_time = time.time()

    print((end_time - start_time)/no_of_urls, 's per url')



