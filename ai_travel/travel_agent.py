import streamlit as st
from ai_travel.weather_agent import get_weather
from ai_travel.route_agent import get_route

def get_info_mock(start_city, end_city, start_time)-> list[dict]:
    data = [{'City': 'Navi Mumbai', 'Arrival Time': '2025-09-20T11:26:08', 'Time Taken': '0h 21m', 'Distance (km)': 20, 'Weather': '☀️ Clear skies and sunshine.'}, 
            {'City': 'Panvel', 'Arrival Time': '2025-09-20T11:46:08', 'Time Taken': '0h 21m', 'Distance (km)': 20, 'Weather': '☀️ Clear skies and sunny weather.'}, 
            {'City': 'Kharghar', 'Arrival Time': '2025-09-20T12:01:08', 'Time Taken': '0h 16m', 'Distance (km)': 15, 'Weather': '☀️ Clear skies and sunny weather.'}, 
            {'City': 'Belapur', 'Arrival Time': '2025-09-20T12:17:08', 'Time Taken': '0h 8m', 'Distance (km)': 8, 'Weather': '☁️ Partly cloudy sky with no rain expected.'},
            {'City': 'Vashi', 'Arrival Time': '2025-09-20T12:25:08', 'Time Taken': '0h 7m', 'Distance (km)': 7, 'Weather': '☀️ Clear skies and sunshine.'}]
    
    return data

st.cache_data
def get_info(start_city, end_city, start_time)-> list[dict]:
    """
    Retrieves route and weather information for a journey between two cities.
    Args:
        start_city (str): The name of the starting city.
        end_city (str): The name of the destination city.
        start_time (str): The departure time in ISO format.
    Returns:
        pandas.DataFrame: A DataFrame containing route segments with columns:
            - "City": Destination city name.
            - "Arrival Time": Estimated arrival time in ISO format.
            - "Time Taken": Time taken to reach the city segment.
            - "Distance (km)": Distance to the destination city in kilometers.
            - "Weather": Weather summary and icon at arrival time.
    Notes:
        - Requires `get_route` and `get_weather` helper functions.
        - If no route is found, returns an empty DataFrame.
    """
    cities = get_route(start_city, end_city, start_time)
    table_data = []
    # with st.status("Fetching route and weather info...", expanded=True) as status:
    #     status.update(label="Getting route...", state="running")
    #     # Route fetching is already done above
    #     status.update(label="Getting weather for each city...", state="running")
    #     # Weather fetching is done in the loop below
    #     # The rest of the code continues as normal
    #     status.update(label="Done!", state="complete")
    if cities := cities.get("segments", []) if cities else []:
        # Fetch weather for each city at estimated arrival time
        # 'start_city', 'destination_city', 'distance_to_destination', 'arrival_time', 'time_taken'
        weather_results = []
        for city_info in cities:
            city_name = city_info[1]  # Destination city
            arrival_time = city_info[3]  # Arrival time in ISO format
            weather = get_weather(city_name, arrival_time)
            weather_results.append((city_name, weather))
        for i, city_info in enumerate(cities):
            city_name = city_info[1]
            distance = city_info[2]
            arrival_time = city_info[3]
            weather = weather_results[i][1] if i < len(weather_results) else {}
            weather_summary = weather.get('summary', 'No data')
            weather_icon = weather.get('icon', '')
            table_data.append({
                "City": city_name,
                "Arrival Time": arrival_time,
                "Time Taken": city_info[4] if len(city_info) > 4 else "N/A",
                "Distance (km)": distance,
                "Weather": f"{weather_icon} {weather_summary}"
            })
    
    return table_data
