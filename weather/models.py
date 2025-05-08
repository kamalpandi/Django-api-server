from django.db import models

# Create your models here.

class FullWeatherReport(models.Model):
    city_name = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
    coord = models.JSONField()
    weather = models.JSONField()
    main = models.JSONField()
    wind = models.JSONField()
    clouds = models.JSONField()
    sys = models.JSONField()
    base = models.CharField(max_length=50)
    visibility = models.IntegerField()
    dt = models.BigIntegerField()
    timezone = models.IntegerField()
    cod = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class EssentialWeatherReport(models.Model):
    coordinate = models.CharField(max_length=100)  # Storing as a string, since it's a pair of lat, lon.
    country_code = models.CharField(max_length=10)  # Country code (e.g., 'IN')
    humidity = models.IntegerField()  # Percentage of humidity
    pressure = models.IntegerField()  # Atmospheric pressure
    temp = models.CharField(max_length=50)  # Temperature as a string (e.g., "307.9K")

    def __str__(self):
        return f"Weather Report for {self.country_code} at coordinates {self.coordinate}"