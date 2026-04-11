# OpenWeatherAPI 3-day CLI Forecast

> A CLI tool to return a 3-day weather forecast for any city.

---

## What it does
Takes a city name as input, calls the OpenWeatherMap API, and prints a 
formatted 3-day forecast to the terminal. Saves output to forecast.json 
and forecast.csv.

## Inputs
- City name (command line input)

## Outputs
- Formatted console output
- forecast.json
- forecast.csv

## Success criteria
- Returns forecast for any valid city
- Handles errors gracefully (city not found, API failure)
- API key loaded from .env, never hardcoded