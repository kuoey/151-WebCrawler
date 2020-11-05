from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper, subdomain, bigBook, print50, uniq_url, maximumWordCount, returnLink
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                print("New test starts here")
                # print(subdomain.items())
                # count of all the subdomains (question #4)
                for i in sorted(subdomain.keys()):
                    print(i, ":", subdomain[i])

                # for i, j in sorted(subdomain.items()):
                # print(i, ", ", len(j), ": ", j)
                print("Total number of unique urls: ", len(uniq_url))  # question #1 (how many unique url there is yuh)
                # print(uniq_url)
                print50(bigBook)  # prints top 50 most frequent words
                print("Max word:", maximumWordCount)
                print("Max word link:", returnLink)
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
