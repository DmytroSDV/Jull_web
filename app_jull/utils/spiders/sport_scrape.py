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

from news.models import SportNews

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customs.custom_logger import my_logger

SPORT_NEWS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "sport_news.json"
)
BASE_URL = "https://gazetainfo.com"


class SportItem(Item):
    title = Field()
    sport_url = Field()
    img_url = Field()
    content = Field()
    date_of = Field()
    time_of = Field()


class DataPipeline:
    news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.news.append(dict(adapter))

    def close_spider(self, spider):
        # with open(SPORT_NEWS_FILE, "w", encoding="utf-8") as fd:
        #     json.dump(self.news, fd, ensure_ascii=False, indent=4)
        my_logger.log(f"{len(self.news)} sport scrapped len", 20)

        for item in self.news:
            if not SportNews.objects.filter(title=item["title"]).exists():
                article = SportNews(
                    title=item["title"].replace("/", "").replace("\\", ""),
                    sport_url=item["sport_url"],
                    image_url=item["img_url"],
                    date_of=item["date_of"],
                    time_of=item["time_of"],
                    content=item["content"].replace("/", "").replace("\\", ""),
                )
                article.save()


class SportSpider(scrapy.Spider):
    name = "get_news"
    allowed_domains = ["gazetainfo.com"]
    start_urls = ["https://gazetainfo.com/sport"]

    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}, "DOWNLOAD_DELAY": 0.2}

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
            sport_url = block.xpath(
                './/following-sibling::div[@class="eTitle"]/a/@href'
            ).get()
            date_of = response.xpath(
                '//div[@class="eDetailsDT"]/span[@class="e-date"]/span[@class="ed-value"]/text()'
            ).get()
            time_of = response.xpath(
                '//div[@class="eDetailsDT"]/span[@class="e-date"]/span[@class="ed-value"]/@title'
            ).get()

            yield scrapy.Request(
                url=f"{BASE_URL}{sport_url}",
                callback=self.parse_sport_news,
                meta={
                    "title": title,
                    "sport_url": f"{BASE_URL}{sport_url}",
                    "date_of": date_of,
                    "time_of": time_of,
                },
            )

            if self.max_requests is not None:
                self.request_count += 1
                if self.request_count >= self.max_requests:
                    return

        next_pages = response.xpath(
            '//div[@class="catPages1"]//a[@class="swchItem"]/@href'
        ).getall()
        for next_page in next_pages:
            next_page = f"{BASE_URL}{next_page}"
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_sport_news(self, response):
        title = response.meta["title"]
        sport_url = response.meta["sport_url"]
        date_of = response.meta["date_of"]
        time_of = response.meta["time_of"]

        img_url = response.xpath('//div[@class="imgone"]/img/@src').get()
        content = " ".join(
            response.xpath('//td[@class="eMessage"]//text()').getall()
        ).strip()

        yield SportItem(
            title=title,
            sport_url=sport_url,
            img_url=f"{BASE_URL}{img_url}",
            content=content,
            date_of=date_of,
            time_of=time_of,
        )


def run_spider(max_requests=60):
    process = CrawlerProcess()
    process.crawl(SportSpider, max_requests=max_requests)
    process.start()


if __name__ == "__main__":
    run_spider()
