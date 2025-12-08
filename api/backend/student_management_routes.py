import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(layout='wide')

SideBarLinks()

st.title('📚 Available Study Sessions')

# ============================================
# 1. Display All Upcoming Study Sessions
# ============================================
st.write("## All Upcoming Study Sessions")

if st.button("Load All Sessions", type="primary", use_container_width=True):
    try:
        url = "http://web-api:4000/sessions"
        response = requests.get(url)
        sessions = response.json()
        
        if sessions and len(sessions) > 0:
            st.success(f"Found {len(sessions)} study sessions!")
            df = pd.DataFrame(sessions)
            
            # Format datetime columns for better display
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No study sessions found.")
    except Exception as e:
        st.error(f"Error loading sessions: {e}")

st.write("---")

# ============================================
# 2. Search Sessions by Building
# ============================================
st.write("## 🔍 Search by Location")

col1, col2 = st.columns(2)

with col1:
    building = st.selectbox("Select building:", 
                           ["All Buildings", "Snell Library", "Curry Student Center", 
                            "Forsyth Building", "Ryder Hall"])

with col2:
    room = st.text_input("Room number (optional):", "")

if st.button("Search by Location", use_container_width=True):
    try:
        building_param = "" if building == "All Buildings" else building
        url = f"http://web-api:4000/sessions/location?building={building_param}&room={room}"
        results = requests.get(url).json()
        
        if results and len(results) > 0:
            st.success(f"Found {len(results)} sessions!")
            df = pd.DataFrame(results)
            
            # Format times
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sessions found for this location.")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")

# ============================================
# 3. Search Sessions by Date
# ============================================
st.write("## 📅 Search by Date")

session_date = st.date_input("Select date:", datetime.now())

if st.button("Search by Date", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/date/{session_date}"
        results = requests.get(url).json()
        
        if results and len(results) > 0:
            st.success(f"Found {len(results)} sessions on {session_date}")
            df = pd.DataFrame(results)
            
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sessions found for this date.")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")

# ============================================
# 4. Session Details View
# ============================================
st.write("## 📋 View Session Details")

session_id = st.number_input("Enter Session ID:", min_value=1000, max_value=1100, value=1001, step=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("Get Session Details", use_container_width=True):
        try:
            # Get session basic info
            url = f"http://web-api:4000/sessions/{session_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                session = response.json()
                
                if session and 'sessionID' in session:
                    st.success("Session found!")
                    
                    # Display session info in columns
                    info_col1, info_col2, info_col3 = st.columns(3)
                    
                    with info_col1:
                        st.write("**📅 Session Information:**")
                        st.write(f"Date: {session.get('date', 'N/A')}")
                        start_time = pd.to_datetime(session.get('startTime')).strftime('%I:%M %p') if session.get('startTime') else 'N/A'
                        end_time = pd.to_datetime(session.get('endTime')).strftime('%I:%M %p') if session.get('endTime') else 'N/A'
                        st.write(f"Time: {start_time} - {end_time}")
                    
                    with info_col2:
                        st.write("**🏢 Location:**")
                        st.write(f"Building: {session.get('building', 'N/A')}")
                        st.write(f"Room: {session.get('room', 'N/A')}")
                        st.write(f"Capacity: {session.get('capacity', 'N/A')}")
                    
                    with info_col3:
                        st.write("**📊 Status:**")
                        status = "✅ Available" if session.get('status') == 1 else "❌ Unavailable"
                        st.write(status)
                    
                    st.write("---")
                    
                    # Get topics covered
                    st.write("**📚 Topics Covered:**")
                    try:
                        topics_url = f"http://web-api:4000/sessions/{session_id}/topics"
                        topics_response = requests.get(topics_url)
                        
                        if topics_response.status_code == 200:
                            topics = topics_response.json()
                            
                            if topics and len(topics) > 0:
                                for topic in topics:
                                    course_info = f"{topic.get('department', '')} {topic.get('courseName', '')}" if 'department' in topic else ""
                                    st.write(f"• {topic.get('name', 'Unknown topic')} ({course_info})")
                            else:
                                st.info("No topics listed for this session")
                        else:
                            st.info("Topics information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load topics: {e}")
                    
                    # Get attending TAs
                    st.write("**👨‍🏫 Teaching Assistants:**")
                    try:
                        tas_url = f"http://web-api:4000/sessions/{session_id}/tas"
                        tas_response = requests.get(tas_url)
                        
                        if tas_response.status_code == 200:
                            tas = tas_response.json()
                            
                            if tas and len(tas) > 0:
                                for ta in tas:
                                    st.write(f"• {ta.get('firstName', '')} {ta.get('lastName', '')} - {ta.get('email', '')}")
                            else:
                                st.info("No TAs assigned yet")
                        else:
                            st.info("TA information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load TAs: {e}")
                    
                    # Get students enrolled
                    st.write("**👥 Students Enrolled:**")
                    try:
                        students_url = f"http://web-api:4000/sessions/{session_id}/students"
                        students_response = requests.get(students_url)
                        
                        if students_response.status_code == 200:
                            students = students_response.json()
                            
                            if students and len(students) > 0:
                                st.write(f"Total students: {len(students)}")
                                with st.expander("View student list"):
                                    for student in students:
                                        st.write(f"• {student.get('firstName', '')} {student.get('lastName', '')} ({student.get('majorOne', 'N/A')})")
                            else:
                                st.info("No students enrolled yet")
                        else:
                            st.info("Student information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load students: {e}")
                else:
                    st.warning("Session not found.")
            elif response.status_code == 404:
                st.error("Session not found.")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    # Join/Leave session functionality
    st.write("**Join or Leave Session:**")
    
    student_nuid = st.number_input("Enter your NUID:", min_value=100000000, max_value=999999999, value=2345678, step=1)
    
    join_col, leave_col = st.columns(2)
    
    with join_col:
        if st.button("Join Session", type="primary", use_container_width=True):
            try:
                url = f"http://web-api:4000/sessions/{session_id}/join"
                data = {"nuID": student_nuid}
                response = requests.post(url, json=data)
                
                if response.status_code == 201:
                    st.success("Successfully joined the session!")
                elif response.status_code == 400:
                    st.warning(response.json().get('error', 'Already enrolled or invalid request'))
                elif response.status_code == 404:
                    st.error(response.json().get('error', 'Session or student not found'))
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with leave_col:
        if st.button("Leave Session", use_container_width=True):
            try:
                url = f"http://web-api:4000/sessions/{session_id}/leave"
                data = {"nuID": student_nuid}
                response = requests.delete(url, json=data)
                
                if response.status_code == 200:
                    st.success("Successfully left the session!")
                elif response.status_code == 404:
                    st.warning("Not enrolled in this session or session not found")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {e}")

st.write("---")