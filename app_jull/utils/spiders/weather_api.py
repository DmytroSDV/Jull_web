import requests
import json
import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")
django.setup()


API_KEY = "78c49d0da7041c7c2d9e2de8d0db7caa"
WEATHER_GEO = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "weather_geo.json"
)
WEATHER_INFO = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "weather_info.json"
)
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?"
GEO_CODING_URL = "http://api.openweathermap.org/geo/1.0/direct?"


def get_current_geo(city: str = "Kyiv", limit: int = 1):
    params = {
        "q": city,
        "limit": limit,
        "appid": API_KEY,
    }
    response = requests.get(GEO_CODING_URL, params=params)

    with open(WEATHER_GEO, "w", encoding="utf-8") as fh:
        json.dump(response.json(), fh, ensure_ascii=False, indent=4)


def get_current_weather(units: str = "metric", language: str = "en"):

    with open(WEATHER_GEO, "r", encoding="utf-8") as fh:
        returned_text = json.load(fh)

    if not returned_text:
        return None

    params = {
        "lon": returned_text[0]["lon"],
        "lat": returned_text[0]["lat"],
        "appid": API_KEY,
        "units": units,
        "lang": language,
    }
    next_response = requests.get(CURRENT_WEATHER_URL, params=params)

    with open(WEATHER_INFO, "w", encoding="utf-8") as fh:
        json.dump(next_response.json(), fh, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_current_geo()
    get_current_weather(language="ua")














