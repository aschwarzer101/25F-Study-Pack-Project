import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests 

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()


# set the header of the page
st.header('Course Materials Management')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# select a course from the list of courses retrieved from the API
courses = requests.get('http://api:4000/c/courses').json()
selected_course = st.selectbox("Select a course:", courses, format_func = lambda x: f"{x['course_name']} CRN: {x['crn']}")
st.write(f"You selected: {selected_course['course_name']} (CRN: {selected_course['crn']})")

# upload a new course material (Professor -2 user story)
st.expander("Upload New Course Material", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        resource_name = st.text_input("Resource Name")
        resource_type = st.selectbox("Resource Type", ["PDF", "Video", "Textbook", "URL", "Image", "Other"])
    with col2:
        resource_id = st.text_input("Resource ID")
        upload_date = st.date_input("Upload Date")
    
    description = st.text_area("Description")

    if st.button("Upload Resource"):
        data = {
            "resourceID": resource_id,
            "name": resource_name,
            "type": resource_type,
            "dateUploaded": str(upload_date),
            "description": description,
            "CRN": selected_course['CRN']
        }
        response = requests.post('http://api:4000/c/resource', json=data)
        if response.status_code == 201:
            st.success("Resource uploaded successfully!")
        else:
            st.error("Failed to upload resource.")
            st.error({response.json()})

st.write("---")


# manages course materials (update [Professor 1.4]/delete [Professor 1.3])
st.subheader("Manage Existing Course Materials")
resources = requests.get(f"http://api:4000/c/resources/{selected_course['CRN']}").json()

for resource in resources:
    with st.container():
        col1, col2, col3 = st.columns([3,1, 1])
        with col1:
            st.write(f"**{resource['name']}** ({resource['type']})")
            st.caption(resource['description'] + f" | Uploaded on: {resource['dateUploaded']}")

        # Update resource [Professor 1.4]
        with col2:
            if st.button("Edit", key=f"edit_{resource['resourceID']}"):
                st.session_state[f'editing_{resource["resourceID"]}'] = True
       
       # Delete resource [Professor 1.3]
       with col3:
            if st.button("Delete", key=f"delete_{resource['resourceID']}"):
                response = requests.delete(f"http://api:4000/c/resource/{resource['resourceID']}")
                if response.status_code == 200:
                    st.success("Resource deleted successfully!")
                else:
                    st.error("Failed to delete resource.")

        if st.session_state.get(f'editing_{resource["resourceID"]}', False):
            with st.form(key = f'form_{resource["resourceID"]}'):
                new_name = st.text_input("Resource Name", value=resource['name'])
                new_description = st.text_area("Description", value=resource['description'])

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Save Changes"):
                        update_data = {
                            "name": new_name,
                            "description": new_description
                        }
                        response = requests.put(f"http://api:4000/c/resource/{resource['resourceID']}", json=update_data)
                        if response.status_code == 200:
                            st.success("Resource updated successfully!")
                            st.session_state[f'editing_{resource["resourceID"]}'] = False
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state[f'editing_{resource["resourceID"]}'] = False

        st.divider()