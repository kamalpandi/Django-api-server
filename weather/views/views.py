import os
import json
import urllib.request
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ..models import EssentialWeatherReport, FullWeatherReport
from dotenv import load_dotenv

load_dotenv()


CITIES = [
    "London",
    "Paris",
    "New York",
    "Tokyo",
    "Sydney",
    "Bengaluru",
    "Dubai",
    "Moscow",
]


def weather_view(request):
    """
    Handles rendering the main page on GET and fetching weather data on POST.
    """
    if request.method == "GET":
        return render(request, "weather/index.html", {"cities": CITIES})

    if request.method == "POST":
        try:
            city = request.POST.get("city")

            if not city:
                return HttpResponse("City not provided", status=400)

            if city not in CITIES:
                return HttpResponse(f"City '{city}' not found.", status=404)

            url = f"{os.environ.get('BASE_URL')}?q={city}&appid={os.environ.get('API_KEY')}"
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            temp_kelvin = list_of_data.get("main", {}).get("temp")
            temp_celsius = (
                f"{temp_kelvin - 273.15:.1f}°C" if temp_kelvin is not None else "N/A"
            )

            data = {
                "city": city,
                "country_code": list_of_data.get("sys", {}).get("country", "N/A"),
                "coordinate": f"{list_of_data.get('coord', {}).get('lon')} {list_of_data.get('coord', {}).get('lat')}",
                "temp": temp_celsius,
                "pressure": list_of_data.get("main", {}).get("pressure", "N/A"),
                "humidity": list_of_data.get("main", {}).get("humidity", "N/A"),
            }

            return render(request, "weather/weather_snippet.html", data)

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def index(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            city = body_data.get("city")

            if not city:
                return JsonResponse({"error": "City not provided"}, status=400)

            url = f"{os.environ.get('BASE_URL')}?q={city}&appid={os.environ.get('API_KEY')}"
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
def weather_for_cities(request):
    """
    Fetches weather data for a list of cities provided in a POST request.
    Expects JSON: {"cities": ["London", "Tokyo", "NonExistentCity"]}
    """
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)

            cities = body_data.get("cities")
            if not cities or not isinstance(cities, list):
                return JsonResponse(
                    {"error": "City list not provided or not in correct format"},
                    status=400,
                )

            weather_data_list = []

            for city in cities:
                if not isinstance(city, str) or not city.strip():
                    weather_data_list.append(
                        {"city": city, "error": "Invalid city name provided"}
                    )
                    continue

                url = f"{os.environ.get('BASE_URL')}?q={city}&appid={os.environ.get('API_KEY')}"

                try:
                    source = urllib.request.urlopen(url).read()
                    list_of_data = json.loads(source)

                    if str(list_of_data.get("cod")) != "200":  # API error
                        weather_data_list.append(
                            {
                                "city": city,
                                "error": list_of_data.get("message", "API error"),
                            }
                        )
                    else:
                        temp_kelvin = list_of_data.get("main", {}).get("temp")
                        temp_celsius = (
                            f"{temp_kelvin - 273.15:.2f}°C"
                            if temp_kelvin is not None
                            else "N/A"
                        )

                        data = {
                            "city": city,
                            "country_code": list_of_data.get("sys", {}).get("country"),
                            "coordinate": f"{list_of_data.get('coord', {}).get('lon')} {list_of_data.get('coord', {}).get('lat')}",
                            "temp": temp_celsius,
                            "pressure": list_of_data.get("main", {}).get("pressure"),
                            "humidity": list_of_data.get("main", {}).get("humidity"),
                            "description": (
                                list_of_data.get("weather", [{}])[0].get(
                                    "description", ""
                                )
                                if list_of_data.get("weather")
                                else ""
                            ),
                        }
                        weather_data_list.append(data)

                except urllib.error.HTTPError as e:
                    weather_data_list.append(
                        {
                            "city": city,
                            "error": f"API request failed: {e.code} {e.reason}",
                        }
                    )
                except urllib.error.URLError as e:
                    weather_data_list.append(
                        {"city": city, "error": f"Network error: {e.reason}"}
                    )
                except json.JSONDecodeError:
                    weather_data_list.append(
                        {"city": city, "error": "Failed to decode API response"}
                    )
                except Exception as e:
                    weather_data_list.append(
                        {"city": city, "error": f"Unexpected error: {str(e)}"}
                    )

            return JsonResponse(weather_data_list, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Overall error: {str(e)}"}, status=500)

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

            url = f"{os.environ.get('BASE_URL')}?q={city}&appid={os.environ.get('API_KEY')}"
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            return JsonResponse(list_of_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except urllib.error.HTTPError as e:
            return JsonResponse(
                {"error": f"API request failed: {e.code} {e.reason}"}, status=502
            )
        except urllib.error.URLError as e:
            return JsonResponse({"error": f"Network error: {e.reason}"}, status=503)
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
            if not all(
                [data.get("coordinate"), data.get("country_code"), data.get("temp")]
            ):
                return JsonResponse({"error": "Missing required fields"}, status=400)
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
