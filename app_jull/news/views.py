from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count

# import subprocess

from utils.spiders import articles_scrape
from news.tasks import test_func


def index(request):

    articles = articles_scrape.run_spider.delay(max_requests=3)
    t1 = test_func.delay()
    print(t1)

    return render(
        request,
        "news/index.html",
        context={"articles": articles},
    )
