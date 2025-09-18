import argparse
import requests
import json
import sys

def get_weather(city_name, api_key):
    """Fetches the current weather for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}", file=sys.stderr)
        sys.exit(1)

def display_weather(data):
    """Displays the formatted weather information."""
    if data and data.get("cod") == 200:
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        
        print(f"Weather in {city}, {country}:")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {description}")
    else:
        print("Could not retrieve weather information for the specified city.", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to parse arguments and run the application."""
    parser = argparse.ArgumentParser(description="A simple command-line weather app.")
    parser.add_argument("city", help="The name of the city to get the weather for.")
    parser.add_argument("--api-key", required=True, help="Your OpenWeatherMap API key.")
    
    args = parser.parse_args()
    
    weather_info = get_weather(args.city, args.api_key)
    if weather_info:
        display_weather(weather_info)

if __name__ == "__main__":
    main()