# 3-day CLI Weather Forecast
A command-line tool that fetches a 3-day weather forecast for any city using the OpenWeatherMap API.

Useful for any application or workflow that needs lightweight, dependency-free weather data from the command line.

## Setup
1. Create a new .env file from .env.example.
2. Create a free account on https://www.openweathermap.org
3. Generate a new API key at https://home.openweathermap.org/api_keys
4. Copy the newly generated API key into the .env file on OPEN_WEATHER_API_KEY

Note: New API keys can take up to 2 hours to activate after registration.

## Run
5. In your CLI, run `python3.12 three-day-forecast.py`
6. Enter a city name as prompted. Press `return` or `Enter`.

## Example Output

3-Day Forecast for Paris, FR
--------------------------------------------------
Tue Apr 14          High: 16.7°C        Low: 12.8°C         Scattered clouds
Wed Apr 15          High: 18.2°C        Low: 5.9°C          Broken clouds
Thu Apr 16          High: 19.0°C        Low: 10.2°C         Overcast clouds

## What I learned
Chaining multiple API calls, parsing nested JSON into structured output, and handling edge cases like unresolved city names.