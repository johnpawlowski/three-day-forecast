# import required packages
import requests # type: ignore
import os
import json
import csv
from dotenv import load_dotenv # type: ignore
from collections import Counter
from datetime import datetime

# load the API key from .env into project variable
load_dotenv()
api_key = os.getenv("OPEN_WEATHER_API_KEY")

# API endpoints
COORD_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# get the location coordindates via the Geocoding API
def get_coord(query):
    try:
        response = requests.get(COORD_URL, params={"q": query, "appid": api_key, "units": "metric"})
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"API error: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print("No internet connection.")
        return None
    data = response.json()

    if data == []:
        print(f"{query} not found.\nFor USA: Try using 'City, State, US'\nFor world: Try using 'City, Country'.")
        return None
    else:
        if data[0]["country"]=='US':
            name = f"{data[0]['name']}, {data[0]['state']}, {data[0]['country']}"
        else:
            name = f"{data[0]['name']}, {data[0]['country']}"
        coord = [data[0]["lat"],data[0]["lon"]]
        return coord, name

# get the 5-day / 3-hour forecast via the Forecast 5-Day/3-Hour API
def get_weather(lat,lon):
    try:
        response = requests.get(WEATHER_URL, params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"})
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"API error: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print("No internet connection.")
        return None
    data = response.json()
    weather = data["list"]
    return weather

# parse the date, temp hi/lo, and description from raw weather data
def forecast(weather):

    # create empty data objects
    days = {}
    forecast_output = []

    # iterate through each 3-hour snapshot from the raw weather data
    for snapshot in weather:

        # for each snapshot, parse just the date from the datetime text field ("dt_txt")
        date = snapshot["dt_txt"].split(" ")[0]

        # if the date parsed does not yet exist in the days dictionary...
        if date not in days:
            # ...create a new key of the text date and a value that is a nested dictionary of two keys ("temps" and "descriptions") with values of empty lists
            days[date] = {"temps":[],"descriptions":[]}

        # append the temperature from the snapshot to the list of "temps" for that date
        days[date]["temps"].append(snapshot["main"]["temp"])
        # append the descriptions from the snapshot to the list of "descriptions" for that date
        days[date]["descriptions"].append(snapshot["weather"][0]["description"])

    # iterate through each day in the days dictionary
    ## days.items() gives a key and value at the same time
    ## so date would be the text date and data would be the nested dictionariy of two keys (from the previous loop)
    for date, data in list(days.items())[:3]:

        # set the values to be appended to forecast_output for the respective date
        day_summary = {
            "date": date,
            "min_temp": min(data["temps"]),
            "max_temp": max(data["temps"]),
            "description": Counter(data["descriptions"]).most_common(1)[0][0]
        }

        # append day_summary to forecast_output
        forecast_output.append(day_summary)

    return forecast_output

# get user input for location
location = input("Get a 3-day weather forecast for ")

# use location to query for the location's coordinates
coord_result = get_coord(location)
if coord_result is None:
    print("Could not retrieve coordinates. Exiting.")
    exit()
coordinates, resolved_name = coord_result

# use coordinates to query for raw weather data
weather = get_weather(coordinates[0],coordinates[1])
if weather is None:
    print("Could not retreive weather data. Exiting.")
    exit()

# parse necessary data points from raw weather data
result = forecast(weather)

# print formatted data points in terminal
print(f"3-Day Forecast for {resolved_name}")
print("--------------------------------------------------")
for day in result:
    date = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%a %b %d")
    high = f"High: {day['max_temp']:.1f}°C"
    low = f"Low: {day['min_temp']:.1f}°C"
    description = day["description"].capitalize()
    print(f"{date:<20}{high:<20}{low:<20}{description}")

# output result to json
with open("forecast.json", "w") as f:
    json.dump(result, f, indent=2)

# output result to csv
with open("forecast.csv", "w", newline="") as f:
    writer = csv.DictWriter(f,fieldnames=["date","max_temp","min_temp","description"])
    writer.writeheader()
    writer.writerows(result)