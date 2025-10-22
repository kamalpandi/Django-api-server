from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "todo_site/home.html")


def contact(request):
    return HttpResponse("Contact us!")
