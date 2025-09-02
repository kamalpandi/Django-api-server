from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse(
        "<h1>Development Under Work</h1><p>This page is currently under development. Please check back later.</p>"
    )
