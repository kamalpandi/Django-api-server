# In todo_site/views.py

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'todo_site/home.html') # Make sure you have a home.html template

def contact(request):
    return HttpResponse("Contact us!")