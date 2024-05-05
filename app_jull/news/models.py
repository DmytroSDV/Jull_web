from django.db import models


class ArticleNews(models.Model):
    title = models.CharField(max_length=250)
    article_url = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    date_of = models.CharField(max_length=50)
    time_of = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SienceNews(models.Model):
    title = models.CharField(max_length=250)
    sience_url = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    date_of = models.CharField(max_length=50)
    time_of = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TechnoNews(models.Model):
    title = models.CharField(max_length=250)
    techno_url = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    date_of = models.CharField(max_length=50)
    time_of = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EurCurrency(models.Model):
    bank_name = models.CharField(max_length=250)
    bamk_cash_desk = models.CharField(max_length=250)
    bank_card_online = models.CharField(max_length=250)
    time_set = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)


class UsdCurrency(models.Model):
    bank_name = models.CharField(max_length=250)
    bamk_cash_desk = models.CharField(max_length=250)
    bank_card_online = models.CharField(max_length=250)
    time_set = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)


class SportNews(models.Model):
    title = models.CharField(max_length=250)
    sport_url = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    date_of = models.CharField(max_length=50)
    time_of = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titlev


class WeatherInfo(models.Model):
    oblast = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    lat = models.CharField(max_length=250)
    lon = models.CharField(max_length=250)
    country_code = models.CharField(max_length=250)
    weather_condition = models.CharField(max_length=250)
    weather_icon = models.CharField(max_length=50)
    temperature_current = models.CharField(max_length=250)
    temperature_feels = models.CharField(max_length=250)
    temperature_min = models.CharField(max_length=250)
    temperature_max = models.CharField(max_length=250)
    pressure_sea_level = models.CharField(max_length=250)
    pressure_ground_level = models.CharField(max_length=250)
    humidity = models.CharField(max_length=250)
    wind_speed = models.CharField(max_length=250)
    wind_direction = models.CharField(max_length=250)
    sunrise = models.CharField(max_length=250)
    sunset = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city
