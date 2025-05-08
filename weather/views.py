import json
import urllib.request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EssentialWeatherReport, FullWeatherReport


@csrf_exempt
def index(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            city = body_data.get("city")

            if not city:
                return JsonResponse({"error": "City not provided"}, status=400)

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b6faadd28429358d910f9a620e0edfc1"
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            data = {
                "country_code": list_of_data["sys"]["country"],
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp'] - 273.15}°C",
                "pressure": list_of_data["main"]["pressure"],
                "humidity": list_of_data["main"]["humidity"],
            }
            return JsonResponse(data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


@csrf_exempt
def full_weather_report(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            city = body_data.get("city")

            if not city:
                return JsonResponse({"error": "City not provided"}, status=400)

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b6faadd28429358d910f9a620e0edfc1"
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            return JsonResponse(list_of_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


@csrf_exempt
def save_full_weather_report(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON body
            data = json.loads(request.body)

            # Create a new WeatherReport entry in the database
            FullWeatherReport.objects.create(
                city_name=data.get("name"),
                country=data.get("sys", {}).get("country"),
                coord=data.get("coord"),
                weather=data.get("weather"),
                main=data.get("main"),
                wind=data.get("wind"),
                clouds=data.get("clouds"),
                sys=data.get("sys"),
                base=data.get("base"),
                visibility=data.get("visibility"),
                dt=data.get("dt"),
                timezone=data.get("timezone"),
                cod=data.get("cod"),
            )

            # Return success response
            return JsonResponse({"status": "success"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


@csrf_exempt
def save_essential_weather_report(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON body
            data = json.loads(request.body)
            print(data)
            # Create a new EssentialWeatherReport entry in the database
            EssentialWeatherReport.objects.create(
                coordinate=data.get("coordinate"),
                country_code=data.get("country_code"),
                humidity=data.get("humidity"),
                pressure=data.get("pressure"),
                temp=data.get("temp"),
            )

            # Return success response
            return JsonResponse({"status": "success"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def get_essential_weather_reports(request):
    if request.method == "GET":
        # Retrieve all weather reports from the database
        reports = EssentialWeatherReport.objects.all()

        # Prepare the response data by converting the queryset to a list of dictionaries
        report_data = []
        for report in reports:
            report_data.append(
                {
                    "coordinate": report.coordinate,
                    "country_code": report.country_code,
                    "humidity": report.humidity,
                    "pressure": report.pressure,
                    "temp": report.temp,
                }
            )

        # Return the data as JSON
        return JsonResponse(report_data, safe=False)
    return JsonResponse({"error": "Only GET method allowed"}, status=405)


def get_full_weather_report(request):
    if request.method == "GET":
        # Retrieve all full weather reports from the database
        reports = FullWeatherReport.objects.all()

        # Prepare the response data by converting the queryset to a list of dictionaries
        report_data = []
        for report in reports:
            report_data.append(
                {
                    "city_name": report.city_name,
                    "country": report.country,
                    "coord": report.coord,  # Coordinate stored as a JSON field
                    "weather": report.weather,  # Weather stored as a JSON field
                    "main": report.main,  # Main data stored as a JSON field
                    "wind": report.wind,  # Wind data stored as a JSON field
                    "clouds": report.clouds,  # Clouds data stored as a JSON field
                    "sys": report.sys,  # System data stored as a JSON field
                    "base": report.base,
                    "visibility": report.visibility,
                    "dt": report.dt,
                    "timezone": report.timezone,
                    "cod": report.cod,
                    "created_at": report.created_at,
                }
            )

        # Return the data as JSON
        return JsonResponse(report_data, safe=False)
    return JsonResponse({"error": "Only GET method allowed"}, status=405)
