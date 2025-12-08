import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Available Study Sessions')

st.write('\n\n')
st.write('## Find a Study Session')

# ============================================
# 1. Display All Study Sessions
# ============================================
st.write("## All Upcoming Study Sessions")

if st.button("Load All Sessions", type="primary", use_container_width=True):
    try:
        # API call to get all study sessions
        url = "http://web-api:4000/sessions"
        response = requests.get(url)
        sessions = response.json()
        
        if sessions:
            st.success(f"Found {len(sessions)} study sessions!")
            # Convert to DataFrame for better display
            df = pd.DataFrame(sessions)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No study sessions found.")
    except Exception as e:
        st.error(f"Error loading sessions: {e}")

# ============================================
# 2. Search Sessions by Location
# ============================================
st.write("## Search by Location")

building = st.text_input("Enter building name:", "")
room = st.text_input("Enter room number:", "")

if st.button("Search by Location", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/location?building={building}&room={room}"
        results = requests.get(url).json()
        
        if results:
            st.success("Sessions found!")
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.info("No sessions found for this location.")
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================
# 3. Search Sessions by Date
# ============================================
st.write("## Search by Date")

session_date = st.date_input("Select date:")

if st.button("Search by Date", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/date/{session_date}"
        results = requests.get(url).json()
        
        if results:
            st.success(f"Found {len(results)} sessions on {session_date}")
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.info("No sessions found for this date.")
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================
# 4. Search Sessions by Course (CRN)
# ============================================
st.write("## Search by Course")

crn = st.number_input("Enter Course CRN:", min_value=0, step=1)

if st.button("Search by Course", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/course/{crn}"
        results = requests.get(url).json()
        
        if results:
            st.success(f"Found sessions for CRN {crn}")
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.info("No sessions found for this course.")
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================
# 5. Interactive Map of Study Locations
# ============================================
st.write("## Map of Study Locations")

if st.checkbox("Show Session Locations on Map"):
    try:
        # Get all study locations with their sessions
        url = "http://web-api:4000/locations"
        locations = requests.get(url).json()
        
        if locations:
            # You'll need actual lat/lon coordinates for your buildings
            # This is a placeholder - replace with real coordinates
            map_data = []
            for loc in locations:
                map_data.append({
                    "lat": 42.3398,  # Example: Northeastern latitude
                    "lon": -71.0892,  # Example: Northeastern longitude
                    "building": loc.get("building", ""),
                    "room": loc.get("room", ""),
                    "capacity": loc.get("capacity", 0)
                })
            
            df = pd.DataFrame(map_data)
            st.map(df)
            st.write("Study Locations:")
            st.dataframe(df)
        else:
            st.warning("No locations found.")
    except Exception as e:
        st.error(f"Error loading map data: {e}")

# ============================================
# 6. Session Details View
# ============================================
st.write("## View Session Details")

session_id = st.number_input("Enter Session ID:", min_value=0, step=1, key="detail_id")

if st.button("Get Session Details", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/{session_id}"
        session = requests.get(url).json()
        
        if session:
            st.success("Session found!")
            
            # Display session info
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Session Information:**")
                st.write(f"Session ID: {session.get('sessionID')}")
                st.write(f"Date: {session.get('date')}")
                st.write(f"Start Time: {session.get('startTime')}")
                st.write(f"End Time: {session.get('endTime')}")
            
            with col2:
                st.write("**Location:**")
                st.write(f"Building: {session.get('building')}")
                st.write(f"Room: {session.get('room')}")
                st.write(f"Capacity: {session.get('capacity')}")
            
            # Get topics covered
            topics_url = f"http://web-api:4000/sessions/{session_id}/topics"
            topics = requests.get(topics_url).json()
            
            if topics:
                st.write("**Topics Covered:**")
                for topic in topics:
                    st.write(f"- {topic.get('name')}")
            
            # Get attending TAs
            tas_url = f"http://web-api:4000/sessions/{session_id}/tas"
            tas = requests.get(tas_url).json()
            
            if tas:
                st.write("**Teaching Assistants:**")
                for ta in tas:
                    st.write(f"- {ta.get('firstName')} {ta.get('lastName')}")
        else:
            st.warning("Session not found.")
    except Exception as e:
        st.error(f"Error: {e}")