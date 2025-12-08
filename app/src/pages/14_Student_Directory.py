import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="Student & TA Management",
    layout="wide"
)

# Initialize sidebar
SideBarLinks()

st.title("Student & TA Management")
st.markdown("---")

# API endpoint
# API_URL = "http://web-api:4000/ngo/ngos"
API_URL = "http://api:4000"

st.header("Student Management")
st.markdown("---")

student_tab1, student_tab2, student_tab3 = st.tabs(["View Students", "Add Student", "Update/Remove Student"])

# -- View students tab ---
with student_tab1:
    st.subheader("Current Students")
    
    if st.button("Refresh Student List", key="refresh_students"):
        try:
            response = requests.get(f"{API_URL}/sm/students")
            if response.status_code == 200:
                students = response.json()
                if students:
                    df = pd.DataFrame(students)
                    # Display as table
                    st.dataframe(
                        df[['nuID', 'firstName', 'lastName', 'email', 'majorOne', 'classYear']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No students found")
            else:
                st.error(f"Error fetching students: {response.text}")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

# ---------- TAB 2: Add Student ----------
with student_tab2:
    st.subheader("Add New Student")
    
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_nuid = st.text_input("NU ID", placeholder="002345678")
            new_first = st.text_input("First Name")
            new_last = st.text_input("Last Name")
            new_email = st.text_input("Email", placeholder="student@northeastern.edu")
        
        with col2:
            new_grad_year = st.date_input("Graduation Year")
            new_major1 = st.selectbox("Major", 
                ["Computer Science", "Data Science", "Mathematics", "Business", "Other"])
            new_major2 = st.selectbox("Second Major (Optional)", 
                ["None", "Computer Science", "Data Science", "Mathematics", "Business"])
            new_minor = st.selectbox("Minor (Optional)",
                ["None", "Business Administration", "Statistics", "Mathematics"])
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            # Prepare data
            student_data = {
                "nuID": int(new_nuid) if new_nuid else None,
                "firstName": new_first,
                "lastName": new_last,
                "email": new_email,
                "gradYear": str(new_grad_year),
                "majorOne": new_major1,
                "majorTwo": new_major2 if new_major2 != "None" else None,
                "minor": new_minor if new_minor != "None" else None
            }
            
            try:
                response = requests.post(f"{API_URL}/sm/students", json=student_data)  # ← Fixed!
                if response.status_code == 201:
                    st.success(f"✅ Student {new_first} {new_last} added successfully!")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")