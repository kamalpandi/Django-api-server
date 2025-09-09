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

            list_of_data = {
                "sys": {"country": "GB" if city == "London" else "IN"},
                "coord": {"lon": 77.5946, "lat": 12.9716},
                "main": {
                    "temp": 300.15,  # Kelvin
                    "pressure": 1012,
                    "humidity": 80,
                },
            }

            temp_celsius = list_of_data["main"]["temp"] - 273.15
            data = {
                "city": city,
                "country_code": list_of_data["sys"]["country"],
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{temp_celsius:.1f}°C",
                "pressure": list_of_data["main"]["pressure"],
                "humidity": list_of_data["main"]["humidity"],
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


@csrf_exempt  # Add this decorator if you are testing with tools like Postman and not submitting via a Django form
def weather_for_cities(request):
    """
    Fetches weather data for a list of cities provided in a POST request.
    Expects a JSON body with a "cities" key, e.g., {"cities": ["London", "Tokyo", "NonExistentCity"]}.
    """
    if request.method == "POST":
        try:
            # Decode the request body
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            print(type(body_data))
            print("body_data", body_data)
            # Get the list of cities
            cities = body_data.get("cities")
            print("cities", cities)
            if not cities or not isinstance(cities, list):
                return JsonResponse(
                    {"error": "City list not provided or not in correct format"},
                    status=400,
                )

            weather_data_list = []

            for city in cities:
                if not isinstance(city, str) or not city.strip():
                    weather_data_list.append(
                        {
                            "city": city,  # Or a placeholder like "Invalid City Name"
                            "error": "Invalid city name provided in the list.",
                        }
                    )
                    continue  # Skip to the next city

                # Construct the API URL for the current city
                url = f"{os.environ.get('BASE_URL')}?q={city}&appid={os.environ.get('API_KEY')}"

                try:
                    # Make the API request
                    source = urllib.request.urlopen(url).read()
                    list_of_data = json.loads(source)

                    # Check if the API returned an error (e.g., city not found)
                    if (
                        list_of_data.get("cod") != 200
                    ):  # OpenWeatherMap uses 'cod' for status
                        weather_data_list.append(
                            {
                                "city": city,
                                "error": list_of_data.get(
                                    "message", "City not found or API error"
                                ),
                            }
                        )
                    else:
                        # Format the data for the current city
                        data = {
                            "city": city,  # Include the city name for reference
                            "country_code": list_of_data.get("sys", {}).get("country"),
                            "coordinate": f"{list_of_data.get('coord', {}).get('lon')} {list_of_data.get('coord', {}).get('lat')}",
                            "temp": f"{list_of_data.get('main', {}).get('temp', 0) - 273.15:.2f}°C",  # Format to 2 decimal places
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
                    # Handle HTTP errors (e.g., 404 Not Found from OpenWeatherMap)
                    weather_data_list.append(
                        {
                            "city": city,
                            "error": f"API request failed for {city}: {e.code} {e.reason}",
                        }
                    )
                except urllib.error.URLError as e:
                    # Handle URL errors (e.g., network issues)
                    weather_data_list.append(
                        {"city": city, "error": f"URL error for {city}: {e.reason}"}
                    )
                except json.JSONDecodeError:
                    weather_data_list.append(
                        {
                            "city": city,
                            "error": f"Failed to decode API response for {city}.",
                        }
                    )
                except Exception as e:
                    # Catch any other unexpected errors during the API call for a specific city
                    weather_data_list.append(
                        {
                            "city": city,
                            "error": f"An unexpected error occurred for {city}: {str(e)}",
                        }
                    )

            return JsonResponse(
                weather_data_list, safe=False
            )  # safe=False is needed to return a list

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except Exception as e:
            # Catch-all for other errors (e.g., issues with request.body)
            return JsonResponse(
                {"error": f"An overall error occurred: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


# Example of how you might add this to your urls.py:
# from django.urls import path
# from . import views # Assuming your views.py contains the function
#
# urlpatterns = [
#     path('weather-for-cities/', views.weather_for_cities, name='weather_for_cities'),
#     # other paths...
# ]


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
