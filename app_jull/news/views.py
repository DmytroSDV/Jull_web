from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
import random

from news.models import (
    ArticleNews,
    EurCurrency,
    UsdCurrency,
    SienceNews,
    TechnoNews,
    SportNews,
    WeatherInfo,
)


def index(request):

    articles = list(ArticleNews.objects.all())
    eur = list(EurCurrency.objects.all())
    usd = list(UsdCurrency.objects.all())
    siences = list(SienceNews.objects.all())
    technos = list(TechnoNews.objects.all())
    sports = list(SportNews.objects.all())
    weather = list(WeatherInfo.objects.all())

    article_items = random.sample(articles, min(4, len(articles)))
    eur_item = random.sample(eur, min(4, len(eur)))
    usd_item = random.sample(usd, min(4, len(usd)))
    sience_items = random.sample(siences, min(4, len(siences)))
    techno_items = random.sample(technos, min(4, len(technos)))
    sport_items = random.sample(sports, min(4, len(sports)))
    weather_items = random.sample(weather, min(4, len(weather)))

    return render(
        request,
        "news/index.html",
        context={
            "article_items": article_items,
            "eur_item": eur_item,
            "usd_item": usd_item,
            "sience_items": sience_items,
            "techno_items": techno_items,
            "sport_items": sport_items,
            "weather_items": weather_items,
        },
    )


def all_articles(request):
    article_items = ArticleNews.objects.all()

    return render(
        request,
        "news/all_articles.html",
        context={
            "article_items": article_items,
        },
    )


def one_article(request, title):
    article = ArticleNews.objects.filter(title=title).first()

    return render(
        request,
        "news/one_article.html",
        context={
            "article": article,
        },
    )


def all_siences(request):
    sience_items = SienceNews.objects.all()

    return render(
        request,
        "news/all_siences.html",
        context={
            "sience_items": sience_items,
        },
    )


def one_sience(request, title):
    sience = SienceNews.objects.filter(title=title).first()

    return render(
        request,
        "news/one_sience.html",
        context={
            "sience": sience,
        },
    )


def all_technos(request):
    techno_items = TechnoNews.objects.all()

    return render(
        request,
        "news/all_technos.html",
        context={
            "techno_items": techno_items,
        },
    )


def one_techno(request, title):
    techno = TechnoNews.objects.filter(title=title).first()

    return render(
        request,
        "news/one_techno.html",
        context={
            "techno": techno,
        },
    )


def all_sports(request):
    sport_items = SportNews.objects.all()

    return render(
        request,
        "news/all_sports.html",
        context={
            "sport_items": sport_items,
        },
    )


def one_sport(request, title):
    sport = SportNews.objects.filter(title=title).first()

    return render(
        request,
        "news/one_sport.html",
        context={
            "sport": sport,
        },
    )


def all_banks_usd(request):
    usd_item = UsdCurrency.objects.all()

    return render(
        request,
        "news/all_banks_usd.html",
        context={
            "usd_item": usd_item,
        },
    )


def all_banks_eur(request):
    eur_item = EurCurrency.objects.all()

    return render(
        request,
        "news/all_banks_eur.html",
        context={
            "eur_item": eur_item,
        },
    )


def all_weather_cities(request):
    weather_items = WeatherInfo.objects.all()

    return render(
        request,
        "news/all_weather_cities.html",
        context={
            "weather_items": weather_items,
        },
    )


def all_weather_details(request):
    weather_items = WeatherInfo.objects.all()

    return render(
        request,
        "news/all_weather_details.html",
        context={
            "weather_items": weather_items,
        },
    )
