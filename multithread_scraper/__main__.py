from multithread_scraper import scraper_thread

if __name__ == "__main__":
    scraper = scraper_thread.MultithreadScraper(max_threads=30,
                                                input='../data/top_websites.txt',
                                                output='../data/page_data.txt',
                                                driver='../drivers/chromedriver')
