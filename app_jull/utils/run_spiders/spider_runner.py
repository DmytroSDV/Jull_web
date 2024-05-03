import subprocess
import os
import json
from app_jull.celery import app


@app.task
def articles_scrape_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "articles_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def currency_eur_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "currency_eur_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def currency_usd_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "currency_usd_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def sience_scrape_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "sience_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def techno_scrape_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "techno_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def sport_scrape_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "sport_scrape.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


@app.task
def weather_scrape_spider(max_requests=None):

    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "weather_api.py"
    )
    args = ["py", script_path]
    if max_requests is not None:
        args.append(str(max_requests))
    subprocess.run(args, capture_output=False, text=False)


