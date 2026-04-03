from django.urls import path
from . import views

urlpatterns = [
    path('get_todos/', views.get_todos),
    path('create_todo/', views.create_todo),
    path('delete_todo/<int:item_id>/', views.remove_todo),
]