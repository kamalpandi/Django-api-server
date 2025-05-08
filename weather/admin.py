from django.contrib import admin
from .models import EssentialWeatherReport, FullWeatherReport

# Register your models here.
admin.site.register(EssentialWeatherReport)
admin.site.register(FullWeatherReport)
