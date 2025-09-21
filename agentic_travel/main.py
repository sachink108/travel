import streamlit as st
from datetime import datetime

from agentic_travel.login import centered_login_screen
from agentic_travel.html_utils import generate_html_table
from agentic_travel.travel_agent import get_info, get_info_mock

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
    page_icon="✈️",
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
                _time = st.time_input("Time", value=datetime.now().time(), key="start_time")
        
    with st.container():
        end_city = st.text_input(label="Finish/Arrive", label_visibility="collapsed", 
                                placeholder="Finish/Arrive")

travel_datetime = datetime.combine(date, _time)

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
                <p style="text-align:center; color:#34495e; font-size:1.5rem;">
                    <b>From:</b> <span style="color:#2980b9;">{start_city}</span> &nbsp; 
                    <b>To:</b> <span style="color:#27ae60;">{end_city}</span> <br/>
                    <span style="color:#8e44ad;">{travel_datetime.strftime('%A, %d %B %Y at %I:%M %p')}</span>
                </p>
            </div>
            """, unsafe_allow_html=True
        )        
        
        # with st.spinner("Finding the best travel options..."):
        table_data = get_info(start_city, end_city, travel_datetime.isoformat())
        # table_data = get_info_mock(start_city, end_city, travel_datetime.isoformat())
        
        html_table = generate_html_table(table_data)
        st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("""
        <footer style="text-align: center; margin-top: 2rem; font-size: 0.8rem; color: #888;">
            Made with ❤️ by Sachin Kulkarni | <a href="mailto:sachink108@gmail.com">Contact</a>
        </footer>
    """, unsafe_allow_html=True)
    
# poetry run streamlit run .\agentic_travel\main.py --server.port 8502