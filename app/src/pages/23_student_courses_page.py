import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

SideBarLinks()

st.title('🎓 Course Search')

# ============================================
# 1. Search All Courses
# ============================================
st.write("## Browse All Courses")

if st.button("Load All Courses", type="primary", use_container_width=True):
    try:
        url = "http://web-api:4000/courses"
        response = requests.get(url)
        
        if response.status_code == 200:
            courses = response.json()
            
            if courses and len(courses) > 0:
                st.success(f"Found {len(courses)} courses!")
                df = pd.DataFrame(courses)
                
                # Reorder columns for better display
                column_order = ['crn', 'department', 'courseNum', 'name']
                df = df[column_order]
                
                # Rename columns for display
                df.columns = ['CRN', 'Department', 'Course #', 'Course Name']
                
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No courses found.")
        else:
            st.error("Could not load courses")
    except Exception as e:
        st.error(f"Error loading courses: {e}")

st.write("---")


# ============================================
# 3. Search by Course Number
# ============================================
st.write("## 🔢 Search by Course Number")

col1, col2 = st.columns(2)

with col1:
    dept_for_number = st.selectbox("Department:", departments[1:], key="dept_num")

with col2:
    course_num = st.number_input("Course Number:", min_value=1000, max_value=9999, value=3200, step=1)

if st.button("Search by Course Number", use_container_width=True):
    try:
        url = f"http://web-api:4000/courses/search?department={dept_for_number}&courseNum={course_num}"
        response = requests.get(url)
        
        if response.status_code == 200:
            courses = response.json()
            
            if courses and len(courses) > 0:
                st.success("Course found!")
                for course in courses:
                    st.write(f"**{course['department']} {course['courseNum']} - {course['name']}**")
                    st.write(f"CRN: {course['crn']}")
                    
                    # Show professors teaching this course
                    try:
                        prof_url = f"http://web-api:4000/courses/{course['crn']}/professors"
                        prof_response = requests.get(prof_url)
                        
                        if prof_response.status_code == 200:
                            professors = prof_response.json()
                            
                            if professors and len(professors) > 0:
                                st.write("**Professors:**")
                                for prof in professors:
                                    st.write(f"• {prof.get('firstName', '')} {prof.get('lastName', '')} - {prof.get('department', '')}")
                    except:
                        pass
            else:
                st.info("Course not found.")
        else:
            st.error("Error searching course")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")

# ============================================
# 4. Search by CRN
# ============================================
st.write("## 🎯 Search by CRN")

crn_search = st.number_input("Enter CRN:", min_value=10000, max_value=99999, value=12345, step=1)

if st.button("Get Course Details", use_container_width=True):
    try:
        url = f"http://web-api:4000/courses/{crn_search}"
        response = requests.get(url)
        
        if response.status_code == 200:
            course = response.json()
            
            if course and 'crn' in course:
                st.success("Course found!")
                
                # Display course info
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Course Information:**")
                    st.write(f"**{course['department']} {course['courseNum']}**")
                    st.write(f"**{course['name']}**")
                    st.write(f"CRN: {course['crn']}")
                
                with col2:
                    st.write("**Additional Details:**")
                    st.write(f"Department: {course['department']}")
                    st.write(f"Course Number: {course['courseNum']}")
                
                st.write("---")
                
                # Get professors
                st.write("**👨‍🏫 Professors Teaching This Course:**")
                try:
                    prof_url = f"http://web-api:4000/courses/{crn_search}/professors"
                    prof_response = requests.get(prof_url)
                    
                    if prof_response.status_code == 200:
                        professors = prof_response.json()
                        
                        if professors and len(professors) > 0:
                            for prof in professors:
                                with st.expander(f"{prof.get('firstName', '')} {prof.get('lastName', '')}"):
                                    st.write(f"**Department:** {prof.get('department', 'N/A')}")
                                    st.write(f"**Degrees:**")
                                    st.write(f"• {prof.get('degree1', 'N/A')}")
                                    st.write(f"• {prof.get('degree2', 'N/A')}")
                                    st.write(f"• {prof.get('degree3', 'N/A')}")
                        else:
                            st.info("No professors assigned yet")
                except Exception as e:
                    st.warning(f"Could not load professors: {e}")
                
                # Get topics
                st.write("**📚 Topics Covered:**")
                try:
                    topics_url = f"http://web-api:4000/courses/{crn_search}/topics"
                    topics_response = requests.get(topics_url)
                    
                    if topics_response.status_code == 200:
                        topics = topics_response.json()
                        
                        if topics and len(topics) > 0:
                            cols = st.columns(3)
                            for idx, topic in enumerate(topics):
                                with cols[idx % 3]:
                                    st.write(f"• {topic.get('name', 'Unknown')}")
                        else:
                            st.info("No topics listed yet")
                except Exception as e:
                    st.warning(f"Could not load topics: {e}")
                
                # Get study sessions
                st.write("**📅 Upcoming Study Sessions:**")
                try:
                    sessions_url = f"http://web-api:4000/sessions/course/{crn_search}"
                    sessions_response = requests.get(sessions_url)
                    
                    if sessions_response.status_code == 200:
                        sessions = sessions_response.json()
                        
                        if sessions and len(sessions) > 0:
                            sessions_df = pd.DataFrame(sessions)
                            
                            if 'startTime' in sessions_df.columns:
                                sessions_df['startTime'] = pd.to_datetime(sessions_df['startTime']).dt.strftime('%I:%M %p')
                            if 'endTime' in sessions_df.columns:
                                sessions_df['endTime'] = pd.to_datetime(sessions_df['endTime']).dt.strftime('%I:%M %p')
                            if 'date' in sessions_df.columns:
                                sessions_df['date'] = pd.to_datetime(sessions_df['date']).dt.strftime('%Y-%m-%d')
                            
                            st.dataframe(sessions_df[['sessionID', 'date', 'startTime', 'endTime', 'building', 'room']], 
                                       use_container_width=True, hide_index=True)
                        else:
                            st.info("No upcoming study sessions")
                except Exception as e:
                    st.warning(f"Could not load study sessions: {e}")
                
                # Get resources
                st.write("**📖 Course Resources:**")
                try:
                    resources_url = f"http://web-api:4000/courses/{crn_search}/resources"
                    resources_response = requests.get(resources_url)
                    
                    if resources_response.status_code == 200:
                        resources = resources_response.json()
                        
                        if resources and len(resources) > 0:
                            for resource in resources:
                                with st.expander(f"{resource.get('type', 'Resource')}: {resource.get('name', 'Unnamed')}"):
                                    st.write(f"**Description:** {resource.get('description', 'No description')}")
                                    st.write(f"**Type:** {resource.get('type', 'N/A')}")
                                    st.write(f"**Uploaded:** {resource.get('dateUploaded', 'N/A')}")
                        else:
                            st.info("No resources available yet")
                except Exception as e:
                    st.warning(f"Could not load resources: {e}")
                
            else:
                st.warning("Course not found.")
        elif response.status_code == 404:
            st.error("Course not found.")
        else:
            st.error("Error retrieving course details")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")