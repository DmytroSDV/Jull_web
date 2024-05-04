from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count

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
    article_items = ArticleNews.objects.all()[:4]
    eur_item = EurCurrency.objects.all()[:4]
    usd_item = UsdCurrency.objects.all()[:4]
    sience_items = SienceNews.objects.all()[:4]
    techno_items = TechnoNews.objects.all()[:4]
    sport_items = SportNews.objects.all()[:4]
    weather_items = WeatherInfo.objects.all()[:4]

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
