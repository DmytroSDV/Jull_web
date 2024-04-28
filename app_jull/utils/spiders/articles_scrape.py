import os
import django
import sys
import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

from celery import shared_task


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")
django.setup()


ARTICLES_NEWS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "articles_news.json"
)
BASE_URL = "https://gazetainfo.com"


class ArticlesItem(Item):
    title = Field()
    articles_url = Field()
    img_url = Field()
    content = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        with open(ARTICLES_NEWS_FILE, "w", encoding="utf-8") as fd:
            json.dump(self.news, fd, ensure_ascii=False, indent=4)


class ArticlesSpider(scrapy.Spider):
    name = "get_news"
    allowed_domains = ["gazetainfo.com"]
    start_urls = ["https://gazetainfo.com/articles"]

    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

    def __init__(self, max_requests=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_requests = max_requests
        self.request_count = 1

    def parse(self, response):
        news_blocks = response.xpath('//div[@class="eBlockimg"]')

        for block in news_blocks:
            title = block.xpath(
                './/following-sibling::div[@class="eTitle"]/a/text()'
            ).get()
            articles_url = block.xpath(
                './/following-sibling::div[@class="eTitle"]/a/@href'
            ).get()

            yield scrapy.Request(
                url=f"{BASE_URL}{articles_url}",
                callback=self.parse_techno_news,
                meta={"title": title, "articles_url": f"{BASE_URL}{articles_url}"},
            )

            if self.max_requests is not None:
                self.request_count += 1
                if self.request_count >= self.max_requests:
                    break

        next_page = response.xpath(
            '//div[@class="catPages1"]//a[@class="swchItem"]/@href'
        ).get()
        next_page = f"{BASE_URL}{next_page}"
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_techno_news(self, response):
        title = response.meta["title"]
        articles_url = response.meta["articles_url"]

        img_url = response.xpath('//div[@class="imgone"]/img/@src').get()
        content = " ".join(
            response.xpath('//td[@class="eMessage"]//text()').getall()
        ).strip()

        yield ArticlesItem(
            title=title,
            articles_url=articles_url,
            img_url=f"{BASE_URL}{img_url}",
            content=content,
        )


@shared_task
def run_spider(max_requests=None):
    process = CrawlerProcess()
    process.crawl(ArticlesSpider, max_requests=max_requests)
    process.start()
    return DataPipeline().news


if __name__ == "__main__":
    print(run_spider(1))
