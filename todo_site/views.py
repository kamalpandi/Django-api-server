from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    return redirect(settings.FRONTEND_URL)


def contact(request):
    return HttpResponse("Contact us!")
