from multithread_scraper import scraper_thread

MAX_THREADS = 10
INPUT_URL_FILE_LOC = 'data/top_websites.txt'
OUTPUT_URL_FILE_LOC = 'data/page_data.txt'
DRIVER_LOCATION = 'drivers/chromedriver_osx'
if __name__ == "__main__":
    scraper = scraper_thread.MultithreadScraper(max_threads=MAX_THREADS,
                                                input=INPUT_URL_FILE_LOC,
                                                output=OUTPUT_URL_FILE_LOC,
                                                driver=DRIVER_LOCATION)
