import requests
import json
from datetime import datetime

def get_weather_data(city, api_key):
    """Fetches weather data from OpenWeatherMap for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use Celsius for temperature
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Extract relevant information
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "coord": data["coord"],  # Pass coordinates for AQI lookup
            "timestamp": datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing weather data: {e}")
        return None


def get_aqi_data(city, api_key):
    """Fetches AQI data from OpenWeatherMap for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    # OpenWeatherMap's Air Pollution API uses coordinates, not city name directly
    # You'd ideally get coordinates from the weather API response or a geocoding service
    # For simplicity, we'll assume the weather data was fetched first and provides coordinates
    weather_data = get_weather_data(city, api_key)
    if not weather_data:
        return None
    lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching AQI data: {e}")
        return None

# Example usage to test the functions
# Uncomment the following lines to test the functions directly
# if __name__ == "__main__":
#     # Example usage
#     city = "Bengaluru"  # Replace with the desired city
#     api_key = "xxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your OpenWeatherMap API key

#     weather_data = get_weather_data(city, api_key)
#     if weather_data:
#         print(json.dumps(weather_data, indent=4))
#     aqi_data = get_aqi_data(city, api_key)
#     if aqi_data:
#         print(json.dumps(aqi_data, indent=4))
#     # Note: In a real-world scenario, you would want to handle API keys securely
#     # and not hard-code them in your scripts.