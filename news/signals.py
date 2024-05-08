from django.core.signals import request_started
from django.dispatch import receiver
from django.apps import AppConfig
from utils.run_spiders.spider_runner import (
    articles_scrape_spider,
    currency_eur_spider,
    currency_usd_spider,
    sience_scrape_spider,
    techno_scrape_spider,
    sport_scrape_spider,
    weather_scrape_spider,
)


@receiver(request_started)
def run_initial_tasks(sender, **kwargs):
    from news.models import (
        ArticleNews,
        EurCurrency,
        UsdCurrency,
        SienceNews,
        TechnoNews,
        SportNews,
        WeatherInfo,
    )

    if not ArticleNews.objects.exists():
        articles_scrape_spider.delay()

    if not EurCurrency.objects.exists():
        currency_eur_spider.delay()

    if not UsdCurrency.objects.exists():
        currency_usd_spider.delay()

    if not SienceNews.objects.exists():
        sience_scrape_spider.delay()

    if not TechnoNews.objects.exists():
        techno_scrape_spider.delay()

    if not SportNews.objects.exists():
        sport_scrape_spider.delay()

    if not WeatherInfo.objects.exists():
        weather_scrape_spider.delay()
