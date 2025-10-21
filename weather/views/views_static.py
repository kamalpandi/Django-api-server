from django.http import JsonResponse


def get_cities(request):
    return JsonResponse({"cities": ["London", "Tokyo", "madurai", "chennai"]})
