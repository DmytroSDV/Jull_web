import os

from celery.schedules import crontab
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")


app = Celery("app_jull")


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "task1": {
        "task": "utils.run_spiders.spider_runner.articles_scrape_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task2": {
        "task": "utils.run_spiders.spider_runner.currency_eur_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task3": {
        "task": "utils.run_spiders.spider_runner.currency_usd_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task4": {
        "task": "utils.run_spiders.spider_runner.sience_scrape_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task5": {
        "task": "utils.run_spiders.spider_runner.techno_scrape_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task6": {
        "task": "utils.run_spiders.spider_runner.sport_scrape_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
    "task7": {
        "task": "utils.run_spiders.spider_runner.weather_scrape_spider",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(day_of_week="*", hour=0),
    },
}
app.conf.timezone = "UTC"
