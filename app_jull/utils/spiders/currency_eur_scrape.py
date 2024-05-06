import os
import django
import sys
import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from django.utils import timezone


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")
django.setup()

from news.models import EurCurrency

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customs.custom_logger import my_logger


EUR_CURRENCY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "currency_eur_rate.json"
)
BASE_URL = "https://minfin.com.ua"


class EurItem(Item):
    bank_name = Field()
    bank_cash_desk = Field()
    bank_card_online = Field()
    image_url = Field()
    time_set = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        # with open(EUR_CURRENCY_FILE, "w", encoding="utf-8") as fd:
        #     json.dump(self.news, fd, ensure_ascii=False, indent=4)
        # my_logger.log(f"{len(self.news)} eur scrapped len", 20)

        today = timezone.now().date()
        first_entry_date = (
            EurCurrency.objects.first().created_at.date()
            if EurCurrency.objects.exists()
            else None
        )

        if first_entry_date and first_entry_date == today:
            return
        EurCurrency.objects.all().delete()

        for item in self.news:
            eur_item = EurCurrency(
                bank_name=item["bank_name"],
                bamk_cash_desk=item["bank_cash_desk"],
                bank_card_online=item["bank_card_online"],
                image_url=item["image_url"],
                time_set=item["time_set"],
            )
            eur_item.save()


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

            bank_link = row.css(
                "td.js-ex-rates.mfcur-table-bankname a::attr(href)"
            ).get()
            bank_link = f"{BASE_URL}{bank_link}"

            yield scrapy.Request(
                response.urljoin(bank_link),
                callback=self.parse_bank_page,
                meta={
                    "bank_name": bank_name,
                    "bank_cash_desk": bank_cash_desk,
                    "bank_card_online": bank_card_online,
                    "time_set": time_set,
                },
            )

    def parse_bank_page(self, response):
        bank_name = response.meta["bank_name"]
        bank_cash_desk = response.meta["bank_cash_desk"]
        bank_card_online = response.meta["bank_card_online"]
        time_set = response.meta["time_set"]

        # Извлекаем URL изображения логотипа банка
        image_url = response.css("span.c-main_logo img::attr(src)").get()

        yield EurItem(
            bank_name=bank_name,
            bank_cash_desk=bank_cash_desk,
            bank_card_online=bank_card_online,
            time_set=time_set,
            image_url=f"{BASE_URL}{image_url}",
        )


def run_spider():
    process = CrawlerProcess()
    process.crawl(EurSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
