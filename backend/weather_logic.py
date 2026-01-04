from dotenv import load_dotenv
import os
import httpx

load_dotenv(r"C:\Users\User\Documents\Miscellaneous\Coding Projects\Weather-Application\backend\weather_api.env", override = True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

print(f"Loaded OpenWeather API Key: {API_KEY}")

# URL for getting the coordinates of a city
coordinates_url = "http://api.openweathermap.org/geo/1.0/direct"

def build_query(city_name, state_code = None, country_code = None):
    
    # Create a list of parts, filtering out None or empty strings
    parts = [city_name, state_code, country_code]
    
    # join() combines them with commas, [p for p in parts if p] removes empty ones
    q_string = ",".join([p for p in parts if p])
    
    return q_string

# Arguments for the coordinates API (we eventually have to input from frontend)
city_name = "New York City" # Name of the city, required
state_code = "NY" # For US cities only, optional
country_code = "US" # Country code, optional
limit = 1 # Limit the number of results, default is 1, optional

# Format the parameters for httpx request
coordinates_params = {
    "q": build_query(city_name, state_code, country_code),
    "limit": limit,
    "appid": API_KEY
}

# Check if params are as intended
print(f"Coordinates API Params: {coordinates_params}")

# Error handling for the coordinates request
try:
    # Call the coordinates API
    coordinates_response = httpx.get(coordinates_url, params = coordinates_params)

    # Raise an error if the request failed and stops further execution
    coordinates_response.raise_for_status()

    # Parse the JSON response
    coordinates_data = coordinates_response.json()

    print(f"Coordinates Data: {coordinates_data}")
    print(f"Place: {coordinates_data[0]['name']}, Latitude: {coordinates_data[0]['lat']}, Longitude: {coordinates_data[0]['lon']}")
except httpx.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


# URL for getting the weather data using latitude and longitude
weather_url = "https://api.openweathermap.org/data/2.5/weather"

# Arugments for the weather API
latitude = coordinates_data[0]['lat']
longitude = coordinates_data[0]['lon']

# Format the parameters for httpx request
weather_params = {
    "lat": latitude,
    "lon": longitude,
    "appid": API_KEY,
    "units": "metric"  # For the temperature to be displayed in Celsius
}

# Check if params are as intended
print(f"Weather API Params: {weather_params}")

# Error handling for the weather request
try:
    # Call the weather API
    weather_response = httpx.get(weather_url, params = weather_params)

    # Raise an error if the request failed and stops further execution
    weather_response.raise_for_status()

    # Parse the JSON response
    weather_data = weather_response.json()

    print(f"Weather Data: {weather_data}")
    print(f"Current Temperature (in Celsius) in {weather_data['name']}: {weather_data['main']['temp']}°C but feels like {weather_data['main']['feels_like']}°C")
except httpx.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")