import csv
import datetime
import os
import threading
from itertools import zip_longest
from pathlib import Path
from typing import List, Set

import scrapy
import ujson
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer


TOKEN = "sk_7337bd6a9fc24f9a9f06f789ec347910"
PARALLEL_DATES = 100

semaphore = threading.Semaphore(10)


# read tickers to download
def get_supported_tickers() -> List[str]:
	with open('/Users/alon/Study/OpenU/data_science/data_science_project/data/relevant/IEX_supported_tickers.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		tickers = []
		for row in reader:
			tickers.extend(row)
	return tickers


def get_tickers_that_we_have_data_already() -> Set[str]:
	all_tickers_folder = Path('/Users/alon/Study/OpenU/data_science/data_science_project/data/relevant/iex_data')
	used_tickers = set()
	for file in all_tickers_folder.iterdir():
		used_tickers.add(file.stem)
	return used_tickers


class IEXSpider(scrapy.Spider):
	name = 'iex_cloud'
	base_url = "https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=intraday-prices&token={}&exactDate={}&chartIEXOnly=true"

	def start_requests(self):
		delta = datetime.timedelta(days=1)
		date = datetime.date(2019, 3, 1)
		for i in range(PARALLEL_DATES):
			yield scrapy.Request(url=self.base_url.format(",".join(self.tickers), TOKEN, date.strftime("%Y%m%d")), callback=self.parse, meta={'date': date, 'tickers': self.tickers})
			date += delta

	def parse(self, response):
		data = ujson.loads(response.text)
		self.logger.info("got data for %s - date: %s", ",".join(data.keys()), response.meta['date'])
		yield data

		delta = datetime.timedelta(days=PARALLEL_DATES)
		date = response.meta['date']
		date += delta
		if date < datetime.date.today():
			yield scrapy.Request(url=self.base_url.format(",".join(self.tickers), TOKEN, date.strftime("%Y%m%d")), callback=self.parse, meta={'date': date, 'ticker': self.tickers})


def grouper(iterable, n, fillvalue=None):
	args = [iter(iterable)] * n
	return zip_longest(*args, fillvalue=fillvalue)


def run_command(cmd):
	with semaphore:
		os.system(cmd)


if __name__ == "__main__":
	# process = CrawlerProcess(get_project_settings())
	# process.crawl(IEXSpider, ticker='A')
	# process.start(stop_after_crawl=False)  # the script will block here until the crawling is finished
	#
	# process = CrawlerProcess(get_project_settings())
	# process.crawl(IEXSpider, ticker='AAN')
	# process.start(stop_after_crawl=False)  # the script will block here until the crawling is finished


	# for tickers in grouper(get_supported_tickers(), 10):
	# for tickers in grouper(['AAPL', 'A'], 1):
	# process = CrawlerProcess(get_project_settings())
	# for ticker in get_supported_tickers():
	#
	# 	# for ticker in tickers:
	# 	if ticker is not None:
	# 		process.crawl(IEXSpider, ticker=ticker)
	#
	# process.start()  # the script will block here until the crawling is finished
	# # process.start(stop_after_crawl=False)  # the script will block here until the crawling is finished
	used_tickers = get_tickers_that_we_have_data_already()
	all_tickers = set(get_supported_tickers())
	tickers_to_download = list(all_tickers - used_tickers)
	tickers_to_download.sort()

	# for ticker in tickers_to_download:
	# 	threading.Thread(target=run_command, args=(f"sleep 10",)).start()
	# 	# threading.Thread(target=run_command, args=(f"scrapy crawl iex_cloud -a ticker={ticker}",)).start()


	# configure_logging()
	# runner = CrawlerRunner(get_project_settings())
	# for ticker in tickers_to_download:
	# 	runner.crawl(IEXSpider, ticker=ticker)
	#
	# d = runner.join()
	# d.addBoth(lambda _: reactor.stop())
	#
	# reactor.run()

	configure_logging()
	runner = CrawlerRunner(get_project_settings())

	@defer.inlineCallbacks
	def crawl():
		for tickers in grouper(tickers_to_download, 90):
			valid_tickers = [ticker for ticker in tickers if ticker is not None]
			yield runner.crawl(IEXSpider, tickers=valid_tickers)
		reactor.stop()


	crawl()
	reactor.run()
