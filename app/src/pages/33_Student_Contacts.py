import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(
    page_title="Contact Students",
    page_icon=":material/people:",
    layout="wide"
)

# Initialize sidebar
SideBarLinks()

st.title(":material/mail: Contact Students")
st.markdown("View contact information for students you tutor")
st.markdown("---")

API_URL = "http://api:4000"

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
        help="Your 7-digit Northeastern University ID"
    )

with tutor_col2:
    if st.button("Verify Tutor ID", key="verify_tutor", icon=":material/verified_user:"):
        try:
            response = requests.get(f"{API_URL}/sm/peer_tutors")
            if response.status_code == 200:
                tutors = response.json()
                my_tutor = next((t for t in tutors if t.get('nuID') == tutor_nuid), None)
                if my_tutor:
                    st.success(f"Verified: {my_tutor.get('firstName', '')} {my_tutor.get('lastName', '')}")
                else:
                    st.warning("Tutor ID not found in system.")
            else:
                st.error("Could not verify tutor ID")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

st.markdown("---")

# MY STUDENTS SECTION
st.header("My Students", anchor=False, divider="gray")

col1, col2 = st.columns([4, 1])
with col2:
    refresh_btn = st.button("Refresh", use_container_width=True, icon=":material/refresh:")

try:
    response = requests.get(
        f"{API_URL}/pa/tutor_students",
        params={"tutorID": tutor_nuid}
    )
    
    if response.status_code == 200:
        students = response.json()
        
        if students:
            st.caption(f":material/groups: You have {len(students)} student(s)")
            
            for idx, student in enumerate(students):
                with st.container(border=True):
                    col1, col2 = st.columns([2, 2])
                    
                    with col1:
                        st.markdown(f"### :material/person: {student.get('firstName', '')} {student.get('lastName', '')}")
                        st.write(f":material/badge: **Student ID:** {student.get('nuID', 'N/A')}")
                    
                    with col2:
                        st.write(":material/email: **Email:**")
                        st.code(student.get('email', 'N/A'), language=None)
        else:
            st.info(":material/info: No students found. Students will appear here once they are assigned to you.")
    
    elif response.status_code == 404:
        st.warning(":material/warning: Tutor not found. Please verify your Tutor ID.")
    
    else:
        st.error(f":material/error: Error fetching students: {response.text}")

except Exception as e:
    st.error(f":material/error: Connection error: {str(e)}")