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


TECHNO_NEWS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "techno_news.json"
)
BASE_URL = "https://gazetainfo.com"


class TechnoItem(Item):
    title = Field()
    techno_url = Field()
    img_url = Field()
    content = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        with open(TECHNO_NEWS_FILE, "w", encoding="utf-8") as fd:
            json.dump(self.news, fd, ensure_ascii=False, indent=4)


class TechnoSpider(scrapy.Spider):
    name = "get_news"
    allowed_domains = ["gazetainfo.com"]
    start_urls = ["https://gazetainfo.com/techno"]

    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

    def parse(self, response):
        news_blocks = response.xpath('//div[@class="eBlockimg"]')

        for block in news_blocks:
            title = block.xpath(
                './/following-sibling::div[@class="eTitle"]/a/text()'
            ).get()
            techno_url = block.xpath(
                './/following-sibling::div[@class="eTitle"]/a/@href'
            ).get()

            yield scrapy.Request(
                url=f"{BASE_URL}{techno_url}",
                callback=self.parse_techno_news,
                meta={"title": title, "techno_url": f"{BASE_URL}{techno_url}"},
            )

        next_page = response.xpath(
            '//div[@class="catPages1"]//a[@class="swchItem"]/@href'
        ).get()
        next_page = f"{BASE_URL}{next_page}"
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_techno_news(self, response):
        title = response.meta["title"]
        techno_url = response.meta["techno_url"]

        img_url = response.xpath('//div[@class="imgone"]/img/@src').get()
        content = " ".join(
            response.xpath('//td[@class="eMessage"]//text()').getall()
        ).strip()

        yield TechnoItem(
            title=title,
            techno_url=techno_url,
            img_url=f"{BASE_URL}{img_url}",
            content=content,
        )


def run_spider():
    process = CrawlerProcess()
    process.crawl(TechnoSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
