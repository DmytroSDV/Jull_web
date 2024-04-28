import os
import django
import sys
import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")
django.setup()


EUR_CURRENCY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "currency_eur_rate.json"
)


class EurItem(Item):
    bank_name = Field()
    bank_cash_desk = Field()
    bank_card_online = Field()
    time_set = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        with open(EUR_CURRENCY_FILE, "w", encoding="utf-8") as fd:
            json.dump(self.news, fd, ensure_ascii=False, indent=4)


class EurSpider(scrapy.Spider):
    name = "get_currency"
    allowed_domains = ["minfin.com.ua"]
    start_urls = ["https://minfin.com.ua/currency/banks/eur/"]

    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

    def parse(self, response):
        rows = response.css("tr.row--collapse")

        for row in rows:
            bank_name = (
                row.css("td.js-ex-rates.mfcur-table-bankname a::text").get().strip()
            )
            bank_cash_desk = row.css(
                "td.js-ex-rates.mfcur-table-bankname::attr(data-title)"
            ).get()
            bank_card_online = row.css(
                "td.js-ex-rates.mfcur-table-bankname::attr(data-card)"
            ).get()
            time_set = row.css("td.mfcur-table-refreshtime::text").get().strip()

            yield EurItem(
                bank_name=bank_name,
                bank_cash_desk=bank_cash_desk,
                bank_card_online=bank_card_online,
                time_set=time_set,
            )


def run_spider():
    process = CrawlerProcess()
    process.crawl(EurSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
