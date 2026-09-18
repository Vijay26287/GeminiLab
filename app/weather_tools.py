"""Live Destination Weather & Attractions tool for Personal Trip Manager."""

import json
import urllib.parse
import urllib.request
from typing import Optional

# WMO Weather interpretation codes
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}

# Curated attractions for popular travel destinations
CITY_ATTRACTIONS = {
    "paris": [
        "Louvre Museum & Glass Pyramid",
        "Eiffel Tower & Champ de Mars",
        "Musée d'Orsay",
        "Cathédrale Notre-Dame de Paris",
        "Montmartre & Sacré-Cœur Basilica",
        "Arc de Triomphe & Champs-Élysées",
    ],
    "tokyo": [
        "Senso-ji Temple in Asakusa",
        "Shibuya Crossing & Hachiko Statue",
        "Meiji Jingu Shrine & Yoyogi Park",
        "Tsukiji Outer Market (Seafood & Street food)",
        "Tokyo Skytree & Akihabara",
        "Shinjuku Gyoen National Garden",
    ],
    "rome": [
        "Colosseum & Roman Forum",
        "Pantheon & Piazza Navona",
        "Trevi Fountain",
        "Vatican City (St. Peter's Basilica & Sistine Chapel)",
        "Spanish Steps & Villa Borghese",
    ],
    "new york": [
        "Central Park & Bethesda Terrace",
        "Empire State Building & Top of the Rock",
        "Metropolitan Museum of Art (The Met)",
        "Statue of Liberty & Ellis Island",
        "High Line & Hudson Yards",
    ],
}


def get_destination_weather(city: str, date_range: Optional[str] = None) -> dict:
    """Fetch real-time live weather forecast and top attractions for a destination city.

    Args:
        city: Name of the city (e.g., 'Paris', 'Tokyo', 'Rome', 'New York').
        date_range: Optional date or date range description.

    Returns:
        A dictionary with live weather data (temperature C/F, weather condition, forecast) and recommended attractions.
    """
    city_clean = city.strip()
    try:
        # 1. Geocode city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_clean)}&count=1"
        with urllib.request.urlopen(geo_url, timeout=5) as resp:
            geo_data = json.loads(resp.read().decode())
        
        if not geo_data.get("results"):
            return {"error": f"Could not find geographic coordinates for city '{city_clean}'."}
        
        res = geo_data["results"][0]
        lat = res["latitude"]
        lon = res["longitude"]
        country = res.get("country", "")
        formatted_name = f"{res.get('name', city_clean)}, {country}".strip(", ")

        # 2. Fetch live weather & 7-day forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode"
            f"&timezone=auto"
        )
        with urllib.request.urlopen(weather_url, timeout=5) as resp:
            weather_data = json.loads(resp.read().decode())

        curr = weather_data.get("current_weather", {})
        temp_c = curr.get("temperature", 0.0)
        temp_f = round((temp_c * 9 / 5) + 32, 1)
        wcode = curr.get("weathercode", 0)
        condition = WEATHER_CODES.get(wcode, "Clear/Partly Cloudy")
        windspeed = curr.get("windspeed", 0.0)

        daily = weather_data.get("daily", {})
        forecast_list = []
        if daily and "time" in daily:
            times = daily["time"]
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            precip_probs = daily.get("precipitation_probability_max", [])
            wcodes = daily.get("weathercode", [])
            for idx in range(min(5, len(times))):
                forecast_list.append({
                    "date": times[idx],
                    "max_temp_c": max_temps[idx] if idx < len(max_temps) else None,
                    "min_temp_c": min_temps[idx] if idx < len(min_temps) else None,
                    "condition": WEATHER_CODES.get(wcodes[idx], "Clear") if idx < len(wcodes) else "N/A",
                    "precipitation_probability": f"{precip_probs[idx]}%" if idx < len(precip_probs) and precip_probs[idx] is not None else "N/A",
                })

        # 3. Get attractions
        city_lower = city_clean.lower()
        attractions = []
        for k, v in CITY_ATTRACTIONS.items():
            if k in city_lower or city_lower in k:
                attractions = v
                break
        if not attractions:
            attractions = [
                f"Historical city center and old town of {city_clean}",
                f"Local food market and culinary district",
                f"Top landmark museums and cultural galleries in {city_clean}",
                f"Scenic city parks and viewpoint panoramas",
            ]

        return {
            "status": "success",
            "city": formatted_name,
            "current_weather": {
                "temperature_c": temp_c,
                "temperature_f": temp_f,
                "condition": condition,
                "windspeed_kmh": windspeed,
            },
            "five_day_forecast": forecast_list,
            "recommended_attractions": attractions,
        }

    except Exception as e:
        return {
            "error": f"Failed to fetch weather for '{city_clean}': {str(e)}"
        }
