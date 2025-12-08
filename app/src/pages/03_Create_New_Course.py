import streamlit as st
import requests

st.title("Manage Courses")

tab1, tab2 = st.tabs(["Create New Course", "View/Edit Courses"])

with tab1:
    st.subheader("Create New Course")
    
    # Create new course [Professor-5]
    with st.form("create_course_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            crn = st.number_input("CRN")
            course_num = st.number_input("Course Number")
        
        with col2:
            course_name = st.text_input("Course Name")
            department = st.text_input("Department")
        
        submitted = st.form_submit_button("Create Course")
        
        if submitted:
            data = {
                "CRN": crn,
                "courseNum": course_num,
                "name": course_name,
                "department": department
            }
            
            response = requests.post('http://api:4000/c/course', json=data)
            
            if response.status_code == 201:
                st.success(f"Course '{course_name}' created successfully!")
            else:
                st.error(f"Error: {response.json()}")

with tab2:
    st.subheader("Your Courses")
    
    # Get all courses for this professor
    courses = requests.get(f'http://api:4000/c/professor/{st.session_state["ProfessorID"]}/courses').json()
    
    for course in courses:
        with st.expander(f"{course['name']} - CRN: {course['CRN']}"):
            # Get course details (GET /course/<crn>)
            details = requests.get(f'http://api:4000/c/course/{course["CRN"]}').json()
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Department:** {details['department']}")
                st.write(f"**Course Number:** {details['courseNum']}")
            with col2:
                st.write(f"**CRN:** {details['CRN']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("View Materials", key=f"mat_{course['CRN']}"):
                    st.session_state['selected_crn'] = course['CRN']
                    st.switch_page('pages/Professor_Course_Materials.py')
            with col2:
                if st.button("View Analytics", key=f"ana_{course['CRN']}"):
                    st.session_state['selected_crn'] = course['CRN']
                    st.switch_page('pages/Professor_Student_Analytics.py')