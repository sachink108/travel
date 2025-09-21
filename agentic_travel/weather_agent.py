"""
weather_agent.py

This module provides functionality for retrieving and processing weather data for travel destinations.

Features:
- Fetch weather data for specific locations.
- Process and format weather information for display.
- Integrate weather data into travel planning workflows.

Dependencies:
- Requires external APIs or libraries for weather data retrieval.
- Utilizes datetime for handling time-related operations.

Usage:
- Import the module and call the relevant functions to fetch and process weather data.

"""

import json
import streamlit as st
from agentic_travel.ai_client import client

@st.cache_data
def weather_icon(weather):
    weather = weather.lower()
    if "rain" in weather:
        return "🌧️"
    elif "cloud" in weather:
        return "☁️"
    elif "sun" in weather or "clear" in weather:
        return "☀️"
    elif "snow" in weather:
        return "❄️"
    elif "storm" in weather or "thunder" in weather:
        return "⛈️"
    elif "fog" in weather or "mist" in weather or "haze" in weather:
        return "🌫️"
    elif "wind" in weather or "breeze" in weather:
        return "💨"
    elif "drizzle" in weather:
        return "🌦️"
    elif "hail" in weather:
        return "🌨️"
    elif "tornado" in weather:
        return "🌪️"
    elif "hot" in weather or "heat" in weather:
        return "🔥"
    elif "cold" in weather or "chilly" in weather or "freezing" in weather:
        return "🥶"
    return ""
   
@st.cache_data
def get_weather(city_name, arrival_time) -> str:
    prompt_weather = (
        f"Return a JSON object with two keys: 'weather' and 'summary'. "
        f"'weather' should be a single word describing the weather in {city_name} at {arrival_time}. "
        f"'summary' should be a very short summary of the weather. "
        f"Example: {{\"weather\": \"Rainy\", \"summary\": \"Light rain expected.\"}}"
    )
    weather_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_weather}]
    )
    weather = weather_response.choices[0].message.content
    json_weather = json.loads(weather)
    json_weather['icon'] = weather_icon(json_weather.get('weather', ''))
    
    return json_weather