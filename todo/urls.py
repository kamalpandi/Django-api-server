from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("del/<str:item_id>", views.remove, name="del"),
]
