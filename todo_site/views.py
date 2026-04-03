from django.shortcuts import redirect
from django.http import HttpResponse


def home(request):
    return redirect("https://django-frontend-two.vercel.app/")


def contact(request):
    return HttpResponse("Contact us!")
