import requests
import json
import os
import django
import sys
from datetime import datetime
from django.utils import timezone
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_jull.settings")
django.setup()

from news.models import WeatherInfo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customs.custom_logger import my_logger

OBLAST_CITIES = {
    "Вінницька область": ["Вінниця"],
    "Волинська область": ["Луцьк"],
    "Дніпропетровська область": ["Дніпро", "Кривий Ріг"],
    "Донецька область": ["Донецьк", "Маріуполь"],
    "Житомирська область": ["Житомир"],
    "Закарпатська область": ["Ужгород"],
    "Запорізька область": ["Запоріжжя", "Мелітополь"],
    "Івано-Франківська область": ["Івано-Франківськ"],
    "Київська область": ["Київ", "Бровари", "Боярка"],
    "Кіровоградська область": ["Кіровоград"],
    "Луганська область": ["Луганськ"],
    "Львівська область": ["Львів"],
    "Миколаївська область": ["Миколаїв"],
    "Одеська область": ["Одеса"],
    "Полтавська область": ["Полтава"],
    "Рівненська область": ["Рівне"],
    "Сумська область": ["Суми"],
    "Тернопільська область": ["Тернопіль"],
    "Харківська область": ["Харків"],
    "Херсонська область": ["Херсон"],
    "Хмельницька область": ["Хмельницький"],
    "Черкаська область": ["Черкаси"],
    "Чернігівська область": ["Чернігів"],
    "Чернівецька область": ["Чернівці"],
}


API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_GEO = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "weather_geo.json"
)
WEATHER_INFO = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "weather_info.json"
)
FINAL_INFO = os.path.join(
    os.path.dirname(__file__), "..", "scrapped_info", "weather_final.json"
)
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?"
GEO_CODING_URL = "http://api.openweathermap.org/geo/1.0/direct?"

WEATHER_ICON_URL_PREFIX = "https://openweathermap.org/img/wn/"
WEATHER_ICON_URL_SUFFIX = "@2x.png"


def get_current_weather(
    city: str = "Луцьк", limit: int = 1, units: str = "metric", language: str = "en"
):
    full_data = []
    result_dict = {}
    params = {
        "q": city,
        "limit": limit,
        "appid": API_KEY,
    }
    response = requests.get(GEO_CODING_URL, params=params)
    # with open(WEATHER_GEO, "w", encoding="utf-8") as fh:
    #     json.dump(response.json(), fh, ensure_ascii=False, indent=4)

    if response.status_code == 200:
        responce_json = response.json()
        result_dict["city"] = responce_json[0]["local_names"]["uk"]
        result_dict["lat"] = str(responce_json[0]["lat"])
        result_dict["lon"] = str(responce_json[0]["lon"])
        result_dict["country_code"] = responce_json[0]["country"]

        params_next = {
            "lon": responce_json[0]["lon"],
            "lat": responce_json[0]["lat"],
            "appid": API_KEY,
            "units": units,
            "lang": language,
        }
        next_response = requests.get(CURRENT_WEATHER_URL, params=params_next)

        # with open(WEATHER_INFO, "w", encoding="utf-8") as fh:
        #     json.dump(next_response.json(), fh, ensure_ascii=False, indent=4)

        if next_response.status_code == 200:
            next_responce_json = next_response.json()
            result_dict["weather_condition"] = next_responce_json["weather"][0][
                "description"
            ]
            result_dict["weather_icon"] = next_responce_json["weather"][0]["icon"]
            result_dict["temperature_current"] = str(next_responce_json["main"]["temp"])
            result_dict["temperature_feels"] = str(
                next_responce_json["main"]["feels_like"]
            )
            result_dict["temperature_min"] = str(next_responce_json["main"]["temp_min"])
            result_dict["temperature_max"] = str(next_responce_json["main"]["temp_max"])
            result_dict["pressure_sea_level"] = str(
                next_responce_json["main"]["pressure"]
            )
            result_dict["pressure_ground_level"] = str(
                next_responce_json["main"].get("grnd_level", None)
            )
            result_dict["humidity"] = str(next_responce_json["main"]["humidity"])
            result_dict["wind_speed"] = str(next_responce_json["wind"]["speed"])
            result_dict["wind_direction"] = str(next_responce_json["wind"]["deg"])

            result_dict["sunrise"] = datetime.fromtimestamp(
                next_responce_json["sys"]["sunrise"]
            ).strftime("%H:%M:%S")

            result_dict["sunset"] = datetime.fromtimestamp(
                next_responce_json["sys"]["sunset"]
            ).strftime("%H:%M:%S")
            result_dict["region"] = next_responce_json["name"]

            full_data.append(result_dict)
        else:
            my_logger.log(f"Error: {response.status_code} \n {response.text}", 40)
    else:
        my_logger.log(f"Error: {response.status_code} \n {response.text}", 40)

    # with open(FINAL_INFO, "w", encoding="utf-8") as fh:
    #     fh.write(json.dumps(full_data, ensure_ascii=False, indent=4))
    return full_data


def weather_api_request():
    today = timezone.now().date()
    first_entry_date = (
        WeatherInfo.objects.first().created_at.date()
        if WeatherInfo.objects.exists()
        else None
    )

    if first_entry_date and first_entry_date == today:
        return
    WeatherInfo.objects.all().delete()

    for oblast, cities in OBLAST_CITIES.items():
        for city in cities:
            returned_data = get_current_weather(city=city, language="ua")

            for item in returned_data:
                weather_middle = item["weather_icon"]
                item_object = WeatherInfo(
                    oblast=oblast,
                    city=item["city"],
                    lat=item["lat"],
                    lon=item["lon"],
                    country_code=item["country_code"],
                    weather_condition=item["weather_condition"],
                    weather_icon=f"{WEATHER_ICON_URL_PREFIX}{weather_middle}{WEATHER_ICON_URL_SUFFIX}",
                    temperature_current=item["temperature_current"],
                    temperature_feels=item["temperature_feels"],
                    temperature_min=item["temperature_min"],
                    temperature_max=item["temperature_max"],
                    pressure_sea_level=item["pressure_sea_level"],
                    pressure_ground_level=item["pressure_ground_level"],
                    humidity=item["humidity"],
                    wind_speed=item["wind_speed"],
                    wind_direction=item["wind_direction"],
                    sunrise=item["sunrise"],
                    sunset=item["sunset"],
                    region=item["region"],
                )
                item_object.save()


if __name__ == "__main__":
    # get_current_weather()
    weather_api_request()
