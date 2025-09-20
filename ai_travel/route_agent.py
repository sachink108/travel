import json
import streamlit as st

from ai_travel.ai_client import client
AVERAGE_SPEED_KMH = 55 # Average speed in km/h

def get_route_mock(start_city, end_city, start_time):
    """
    Get the route between start_city and end_city with estimated arrival times.
    Uses an AI model to generate the route and parse the response.
    Caches the result to avoid redundant API calls.
    """
    return {'segments': [['Delhi', 'Jaipur', '280', '2025-09-20T14:58:49'], ['Jaipur', 'Ajmer', '131', '2025-09-20T17:01:49'], ['Ajmer', 'Udaipur', '266', '2025-09-20T20:05:49'], ['Udaipur', 'Vadodara', '277', '2025-09-21T00:26:49'], ['Vadodara', 'Surat', '153', '2025-09-21T02:48:49'], ['Surat', 'Mumbai', '285', '2025-09-21T07:30:49']]}

@st.cache_data
def get_route(start_city, end_city, start_time):
    # print(f"Getting route from {start_city} {start_time} to {end_city}")
    # Create the prompt for the AI model   
    # Update the prompt to include time taken for travel to the next city
    prompt_route = (
        f"List all major cities between {start_city} and {end_city} in order. "
        "For each segment, provide the starting city, destination city, distance to destination (in km), "
        "estimated arrival time at the destination, and time taken for travel to the next city (in hours and minutes). "
        f"Assume the journey starts at {start_time} and the average speed is {AVERAGE_SPEED_KMH} km/h. "
        "Return the result as a single JSON object with a field 'segments', which is a list of tuples: "
        "['start_city', 'destination_city', 'distance_to_destination', 'arrival_time', 'time_taken'], "
        "where 'arrival_time' is in ISO 8601 format and 'time_taken' is in the format 'Xh Ym'. "
        "Example: {\"segments\": [[\"CityA\", \"CityB\", \"100\", \"2024-06-10T10:30:00\", \"1h 49m\"], [\"CityB\", \"CityC\", \"120\", \"2024-06-10T12:00:00\", \"2h 10m\"]]}"
    )
    
    route_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_route}]
    )
    route_text = route_response.choices[0].message.content

    cities_distances = []
    # Add the start city and its arrival time (which is the start_time)
    cities_distances.append([start_city, start_city, "0", start_time])
    # Parse the response to extract cities, distances, and arrival times
    try:
        cities_distances = json.loads(route_text)
    except json.JSONDecodeError:
        st.error("Error parsing route information. Please try again.")
        return None, None
    return cities_distances

