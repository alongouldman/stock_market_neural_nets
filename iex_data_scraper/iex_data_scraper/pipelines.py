# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class IexDataScraperPipeline:
    """Distribute items across multiple XML files according to their 'year' field"""

    def open_spider(self, spider):
        self.tickers_to_exporters = {}

    def close_spider(self, spider):
        for exporter in self.tickers_to_exporters.values():
            exporter.finish_exporting()

    def _exporter_for_spider(self, ticker):
        if ticker not in self.tickers_to_exporters:
            f = open(f'/Users/alon/Study/OpenU/data_science/data_science_project/data/relevant/iex_data/{ticker}.csv', 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.tickers_to_exporters[ticker] = exporter
        return self.tickers_to_exporters[ticker]

    def process_item(self, item, spider):
        for ticker, data in item.items():
            exporter = self._exporter_for_spider(ticker)
            prices_per_day = data['intraday-prices']
            if prices_per_day:
                for minute in prices_per_day:
                    exporter.export_item(minute)

        return item

        # for ticker, data in data.items():
        #     prices_per_day = data['intraday-prices']
        #
        #     if prices_per_day:
        #         for minute in prices_per_day:
        #             self.logger.info("got data for %s - date: %s, %s", ticker, minute['date'], minute['minute'])
        #             yield minute