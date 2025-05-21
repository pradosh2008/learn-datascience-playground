import json
from utils import get_weather_data, get_aqi_data
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta # For timezone handling

load_dotenv()  # Load environment variables from .env

def main():
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    city = input("Enter city name: ")
    weather_data = get_weather_data(city, api_key)
    if weather_data:
        print("\n--- Weather Information ---")
        print(f"City: {weather_data['city']}")
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Description: {weather_data['description']}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")

        utc_time = datetime.strptime(weather_data['timestamp'], '%Y-%m-%d %H:%M:%S UTC')
        ist_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30)))
        print(f"Report Time: {ist_time.strftime('%Y-%m-%d %H:%M:%S IST')}")

        aqi_data = get_aqi_data(city, api_key)
        if aqi_data:
            print("\n--- Air Quality Information ---")
            # The structure of the AQI data might vary depending on the API
            # This is an example of how to extract information; adjust as needed
            try:
                aqi = aqi_data["list"][0]["main"]["aqi"]
                timestamp = aqi_data["list"][0]["dt"]
                report_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

                utc_time = datetime.utcfromtimestamp(timestamp)
                ist_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30)))
                # You might want to map AQI value to a description (e.g., Good, Moderate, Poor)
                print(f"Air Quality Index (AQI): {aqi}")
                # Components (example)
                components = aqi_data["list"][0]["components"]
                print(f"  Pollutants (Reported at: {ist_time.strftime('%Y-%m-%d %H:%M:%S IST')}):")
                #print lat and long 
                print(f"  Latitude: {weather_data['coord']['lat']}")
                print(f"  Longitude: {weather_data['coord']['lon']}")
                for pollutant, value in components.items():
                    print(f"    {pollutant}: {value} μg/m³")
            except (KeyError, IndexError, TypeError) as e:
                print(f"Report Time: N/A")
                print(f"Error parsing AQI data: {e}")
                print(json.dumps(aqi_data, indent=2))  # Print raw data for debugging
        else:
            print("Could not retrieve AQI data.")
    else:
        print("Could not retrieve weather data. Please check the city name or try again later.")

if __name__ == "__main__":
    main()