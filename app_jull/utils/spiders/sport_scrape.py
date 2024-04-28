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


SPORT_NEWS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "sport_news.json"
)


class NewsItem(Item):
    category = Field()
    title = Field()
    timestamp = Field()
    news_url = Field()
    image_url = Field()
    content = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        with open(SPORT_NEWS_FILE, "w", encoding="utf-8") as fd:
            json.dump(self.news, fd, ensure_ascii=False, indent=4)


class SportSpider(scrapy.Spider):
    name = "get_news"
    allowed_domains = ["sport.ua"]
    start_urls = ["https://sport.ua/uk"]

    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

    def parse(self, response, **kwargs):
        for news in response.xpath(
            "//div[@class='news-items active']//div[@class='item']"
        ):
            category = news.xpath(
                ".//span[contains(@class, 'item-sport')]/text()"
            ).get()
            title = news.xpath(
                ".//div[contains(@class, 'item-title')]/a/span/text()"
            ).get()
            timestamp = news.xpath("./@data-timestamp").get()
            news_url = news.xpath(
                ".//div[contains(@class, 'item-title')]/a/@href"
            ).get()

            yield scrapy.Request(
                news_url,
                callback=self.parse_news,
                meta={"category": category, "title": title, "timestamp": timestamp},
            )

    def parse_news(self, response):
        category = response.meta["category"]
        title = response.meta["title"]
        timestamp = response.meta["timestamp"]
        news_url = response.url
        image_url = response.xpath(
            "//source[@media='(min-width: 1024px)']/@srcset"
        ).get()

        content = response.xpath(
            "//div[@id='news_text']//p/text() | //div[@id='news_text']//h2/text() | //div[@id='news_text']//h3/text()"
        ).getall()
        content = " ".join(content).strip()

        yield NewsItem(
            category=category,
            title=title,
            timestamp=timestamp,
            news_url=news_url,
            image_url=image_url,
            content=content,
        )


def run_spider():
    process = CrawlerProcess()
    process.crawl(SportSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
