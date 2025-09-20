import streamlit as st
from datetime import datetime

from travel.travel_agent import get_info, get_info_mock
from travel.login import centered_login_screen


# Streamlit UI
st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem; /* Adjust this value as needed, 0rem for minimal top space */
                padding-bottom: 0rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    layout="wide",
    page_title="My Travel App",
    page_icon=":travel:",
    initial_sidebar_state="auto",
    
    menu_items={
        'Report a bug': "mailto:sachink108@gmail.com",
        'About': "# This is your personal travel planner and an *extremely* cool app!"
    }
)

# Add a background image to the top of the page
if not st.user.is_logged_in:
    centered_login_screen()
    st.stop()
else:
    st.markdown("<h1 style='text-align: center;'>Travel Genie: Your AI Journey Planner</h1>", unsafe_allow_html=True)
    st.sidebar.write(f"Welcome, {getattr(st.user, 'display_name', st.user.name)}!")
    if st.sidebar.button("Logout", type="secondary", use_container_width=False, key="logout_sidebar", help="Logout", icon="🚪"):
        st.logout()

with st.sidebar:
    st.markdown("---")
    with st.container():
        start_city = st.text_input(label="Start/Depart", label_visibility="collapsed", 
                                placeholder="Start/Depart")
        with st.expander("Date & Time", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", value=datetime.now().date(), key="start_date")
            with col2:
                time = st.time_input("Time", value=datetime.now().time(), key="start_time")
        
    with st.container():
        end_city = st.text_input(label="Finish/Arrive", label_visibility="collapsed", 
                                placeholder="Finish/Arrive")

travel_datetime = datetime.combine(date, time)

go_clicked = st.sidebar.button("Go!", type="primary")
if go_clicked:
    if not start_city or not end_city:
        st.error("Please enter both start and end cities.")
        
    else:
        st.markdown(
            f"""
            <div style="background: linear-gradient(90deg, #e0eafc 0%, #cfdef3 100%); padding: 2rem; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.07); margin-bottom: 1rem;">
                <h2 style="text-align:center; color:#2c3e50; font-size:2.2rem; margin-bottom:0.5rem;">
                    ✈️ Planning your journey...
                </h2>
                <p style="text-align:center; color:#34495e; font-size:1.2rem;">
                    <b>From:</b> <span style="color:#2980b9;">{start_city}</span> &nbsp; 
                    <b>To:</b> <span style="color:#27ae60;">{end_city}</span> <br/>
                    <span style="color:#8e44ad;">{travel_datetime.strftime('%A, %d %B %Y at %I:%M %p')}</span>
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        # st.markdown("---")
        table_data = get_info_mock(start_city, end_city, travel_datetime.isoformat())
        # # Display route and weather information in a table
        st.markdown("""
            <style>
                .travel-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 1.5rem;
                }
                .travel-table th, .travel-table td {
                    border: 1px solid #ddd;
                    padding: 0.75em;
                    text-align: center;
                }
                .travel-table th {
                    background-color: #f4f4f8;
                    color: #333;
                    font-weight: bold;
                }
                .travel-table tr:nth-child(even) {
                    background-color: #fafafa;
                }
                .travel-table tr:hover {
                    background-color: #e6f7ff;
                }
            </style>
        """, unsafe_allow_html=True)

        html_table = "<table class='travel-table'><thead><tr>"
        # Make the table header bold using inline CSS
        html_table += "<style>.travel-table th { font-weight: bold; }</style>"
        for col in ["City", "Arrival Time", "Distance (km)", "Weather"]:
            html_table += f"<th>{col}</th>"
        html_table += "</tr></thead><tbody>"
        for row in table_data:
            html_table += "<tr>"
            html_table += f"<td>{row['City']}</td>"
            arrival_dt = datetime.fromisoformat(row['Arrival Time'])
            formatted_arrival = arrival_dt.strftime('%I:%M %p, %A, %d %B %Y')
            html_table += f"<td>{formatted_arrival}</td>"
            html_table += f"<td>{row['Distance (km)']}</td>"
            html_table += f"<td>{row['Weather']}</td>"
            html_table += "</tr>"
        html_table += "</tbody></table>"

        st.markdown(html_table, unsafe_allow_html=True)
            
