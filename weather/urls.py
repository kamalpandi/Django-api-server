from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("full_report", views.full_weather_report),
    path("save_full_report", views.save_full_weather_report),
    path("save_essential_report", views.save_essential_weather_report),
    path("get_essential_reports", views.get_essential_weather_reports),
    path("get_full_report", views.get_full_weather_report),
]
