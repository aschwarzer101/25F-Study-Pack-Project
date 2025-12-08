import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date

st.set_page_config(
    page_title="Find Tutoring Opportunities",
    page_icon="📚",
    layout="wide"
)

# Initialize sidebar
try:
    from modules.nav import SideBarLinks
    SideBarLinks()
except ImportError:
    st.sidebar.title("Peer Tutor Portal")
    st.sidebar.markdown("---")

st.title("Find Tutoring Opportunities")
st.markdown("Browse and sign up for study sessions that need tutoring help")
st.markdown("---")

API_URL = "http://api:4000"

# Initialize session state for success messages
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = {}

# TUTOR ID INPUT SECTION
st.subheader("Tutor Information", anchor=False)
tutor_col1, tutor_col2 = st.columns([2, 3])

with tutor_col1:
    tutor_nuid = st.number_input(
        "Enter Your Tutor NU ID",
        min_value=1000000,
        max_value=9999999,
        value=3123456,
        step=1,
        key="tutor_nuid_input",
        help="Your 9-digit NUID"
    )
    st.session_state.tutor_id = tutor_nuid

with tutor_col2:
    # Verify tutor exists
    if st.button("Verify Tutor ID", key="verify_tutor", icon=":material/verified_user:"):
        try:
            response = requests.get(f"{API_URL}/sm/peer_tutors")
            if response.status_code == 200:
                tutors = response.json()
                my_tutor = next((t for t in tutors if t.get('nuID') == tutor_nuid), None)
                if my_tutor:
                    st.success(f"Verified: {my_tutor.get('firstName', '')} {my_tutor.get('lastName', '')}")
                else:
                    st.warning("Tutor ID not found in system. You may still sign up for sessions.")
            else:
                st.error("Could not verify tutor ID")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

st.markdown("---")

# FILTERS SECTION
st.header("Filter Sessions", anchor=False, divider="gray")

filter_col1, filter_col2 = st.columns([3, 1])

with filter_col1:
    # Topic filter dropdown
    try:
        topics_response = requests.get(f"{API_URL}/cr/topic")
        
        if topics_response.status_code == 200:
            topics = topics_response.json()
            topic_options = ["All Topics"] + [t.get('name', '') for t in topics]
            selected_topic = st.selectbox(
                "Filter by Topic", 
                topic_options, 
                key="topic_filter"
            )
        else:
            selected_topic = "All Topics"
    except Exception as e:
        st.error(f"Error loading topics: {str(e)}")
        selected_topic = "All Topics"

with filter_col2:
    st.write("")
    refresh_btn = st.button("Refresh", use_container_width=True, icon=":material/refresh:")

# Clear messages button
col_clear1, col_clear2 = st.columns([4, 1])
with col_clear2:
    if st.button("Clear Messages", use_container_width=True, icon=":material/clear_all:"):
        st.session_state.signup_success = {}
        st.rerun()

st.markdown("---")

# AVAILABLE SESSIONS SECTION
st.header("Available Study Sessions", anchor=False, divider="gray")

# Display any persistent success messages at the top
if st.session_state.signup_success:
    for session_id, message in st.session_state.signup_success.items():
        st.success(f":material/check_circle: {message}")

try:
    params = {}
    if selected_topic != "All Topics":
        params["topic"] = selected_topic
    
    response = requests.get(f"{API_URL}/si/study_session", params=params)
    
    if response.status_code == 200:
        sessions = response.json()
        
        if sessions:
            st.caption(f":material/event_available: Found {len(sessions)} session(s)")
            
            for session in sessions:
                session_id = session.get('sessionID', 'N/A')
                
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### :material/event: Session #{session_id}")
                        st.write(f":material/calendar_today: **Date:** {session.get('date', 'N/A')}")
                        st.write(f":material/schedule: **Time:** {session.get('startTime', 'N/A')} - {session.get('endTime', 'N/A')}")
                    
                    with col2:
                        building = session.get('building', 'N/A')
                        room = session.get('room', 'N/A')
                        st.write(f":material/location_on: **Location:** {building}, Room {room}")
                        st.write(f":material/groups: **Capacity:** {session.get('capacity', 'N/A')}")
                        
                        # Fetch topics covered by this session
                        try:
                            all_topics_response = requests.get(f"{API_URL}/cr/topic")
                            if all_topics_response.status_code == 200:
                                all_topics = all_topics_response.json()
                                if all_topics:
                                    st.write(":material/label: **Topics:**")
                                    topic_cols = st.columns(min(len(all_topics[:3]), 3))
                                    for i, topic in enumerate(all_topics[:3]):
                                        with topic_cols[i]:
                                            st.badge(topic.get('name', 'N/A'), icon=":material/topic:")
                        except Exception:
                            pass
                    
                    with col3:
                        # Check if already signed up
                        already_signed_up = session_id in st.session_state.signup_success
                        
                        if already_signed_up:
                            st.success(":material/check: Signed Up!")
                        else:
                            if st.button(
                                "Sign Up",
                                key=f"signup_{session_id}",
                                use_container_width=True,
                                type="primary",
                                icon=":material/person_add:"
                            ):
                                try:
                                    signup_response = requests.post(
                                        f"{API_URL}/pa/tutor_assignments",
                                        json={
                                            "tutorID": tutor_nuid,
                                            "sessionID": session_id
                                        }
                                    )
                                    if signup_response.status_code == 201:
                                        st.session_state.signup_success[session_id] = f"Successfully signed up to tutor Session #{session_id}!"
                                        st.balloons()
                                        st.rerun()
                                    elif signup_response.status_code == 400:
                                        error_msg = signup_response.json().get('error', 'Unknown error')
                                        st.warning(f":material/warning: {error_msg}")
                                    elif signup_response.status_code == 404:
                                        error_msg = signup_response.json().get('error', 'Not found')
                                        st.error(f":material/error: {error_msg}")
                                    else:
                                        st.error(f":material/error: {signup_response.json().get('error', 'Unknown error')}")
                                except Exception as e:
                                    st.error(f":material/error: Connection error: {str(e)}")
        else:
            st.info(":material/event_busy: No study sessions currently available. Check back later!")
    else:
        st.error(f":material/error: Error fetching sessions: {response.text}")

except Exception as e:
    st.error(f":material/error: Connection error: {str(e)}")

st.markdown("---")

# MY TUTORING ASSIGNMENTS SECTION
st.header("My Tutoring Assignments", anchor=False, divider="gray")

try:
    assignments_response = requests.get(
        f"{API_URL}/pa/tutor_assignments",
        params={"tutorID": tutor_nuid}
    )
    
    if assignments_response.status_code == 200:
        assignments = assignments_response.json()
        
        if assignments:
            st.caption(f":material/assignment_turned_in: You have {len(assignments)} active tutoring assignment(s)")
            
            for idx, assignment in enumerate(assignments):
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### :material/assignment: Session #{assignment.get('sessionID', 'N/A')}")
                    
                    with col2:
                        first_name = assignment.get('firstName', '')
                        last_name = assignment.get('lastName', '')
                        if first_name and last_name:
                            st.write(f":material/person: **Tutor:** {first_name} {last_name}")
                        st.write(f":material/badge: **Tutor ID:** {assignment.get('tutorID', 'N/A')}")
                    
                    with col3:
                        if st.button(
                            "Cancel",
                            key=f"cancel_{assignment.get('sessionID')}_{idx}",
                            use_container_width=True,
                            icon=":material/cancel:"
                        ):
                            try:
                                # Call DELETE endpoint to remove tutor assignment
                                cancel_response = requests.delete(
                                    f"{API_URL}/pa/tutor_assignments",
                                    params={
                                        "tutorID": tutor_nuid,
                                        "sessionID": assignment.get('sessionID')
                                    }
                                )
                                if cancel_response.status_code == 200:
                                    # Remove from success messages if present
                                    session_id = assignment.get('sessionID')
                                    if session_id in st.session_state.signup_success:
                                        del st.session_state.signup_success[session_id]
                                    st.success(f":material/check_circle: Successfully cancelled assignment for Session #{session_id}")
                                    st.rerun()
                                else:
                                    error_msg = cancel_response.json().get('error', 'Unknown error')
                                    st.error(f":material/error: Could not cancel: {error_msg}")
                            except Exception as e:
                                st.error(f":material/error: Connection error: {str(e)}")
        else:
            st.info(":material/info: You haven't signed up for any tutoring sessions yet. Browse available sessions above!")
    else:
        st.warning(":material/warning: Could not fetch your assignments. Make sure your Tutor ID is correct.")

except Exception as e:
    st.error(f":material/error: Connection error: {str(e)}")