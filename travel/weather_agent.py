import json
import streamlit as st
from travel.ai_client import client

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
    # Use OpenAI to get weather for the city at the specified time (v1.x API)
    print(f"Getting weather for {city_name} at {arrival_time}")
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