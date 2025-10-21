from django.urls import path
from .views import views, views_static

urlpatterns = [
    path("", views.weather_view, name="weather_view"),
    path("one_city", views.index),
    path("get_essential_reports", views.get_essential_weather_reports),
    path("get_full_report", views.get_full_weather_report),
    path("get_cities", views_static.get_cities),
    path("weather_for_cities", views.weather_for_cities),
    path("full_report", views.full_weather_report),
    path("save_full_report", views.save_full_weather_report),
    path("save_essential_report", views.save_essential_weather_report),
]
