# import logging
# logger = logging.getLogger(__name__)
# import pandas as pd
# import streamlit as st
# from streamlit_extras.app_logo import add_logo
# import world_bank_data as wb
# import matplotlib.pyplot as plt
# import numpy as np
# import plotly.express as px
# from modules.nav import SideBarLinks
# import requests 

# # Call the SideBarLinks from the nav module in the modules directory
# SideBarLinks()

# # set the header of the page
# st.header('Course Materials Management')

# # You can access the session state to make a more customized/personalized app experience
# st.write(f"### Hi, {st.session_state['first_name']}.")

# # Select a course from the list of courses retrieved from the API
# courses = requests.get('http://web-api:4000/cr/course').json()
# selected_course = st.selectbox(
#     "Select a course:",
#     courses,
#     format_func=lambda x: f"{x['course_name']} CRN: {x['crn']}"
# )
# st.write(f"You selected: {selected_course['course_name']} (CRN: {selected_course['crn']})")

# # Upload a new course material (Professor - 2 user story)
# with st.expander("Upload New Course Material", expanded=False):
#     col1, col2 = st.columns(2)

#     with col1:
#         resource_name = st.text_input("Resource Name")
#         resource_type = st.selectbox("Resource Type", ["PDF", "Video", "Textbook", "URL", "Image", "Other"])

#     with col2:
#         resource_id = st.text_input("Resource ID")
#         upload_date = st.date_input("Upload Date")
    
#     description = st.text_area("Description")

#     if st.button("Upload Resource"):
#         data = {
#             "resourceID": resource_id,
#             "name": resource_name,
#             "type": resource_type,
#             "dateUploaded": str(upload_date),
#             "description": description,
#             "CRN": selected_course["crn"]   # FIXED KEY
#         }
#         response = requests.post('http://api:4000/cr/resources', json=data)

#         if response.status_code == 201:
#             st.success("Resource uploaded successfully!")
#         else:
#             st.error("Failed to upload resource.")
#             st.error(response.json())

# st.write("---")

# # Manage course materials (update/delete)
# st.subheader("Manage Existing Course Materials")
# resources = requests.get(f"http://api:4000/cr/resources/{selected_course['crn']}").json()

# for resource in resources:
#     with st.container():
#         col1, col2, col3 = st.columns([3, 1, 1])

#         with col1:
#             st.write(f"**{resource['name']}** ({resource['type']})")
#             st.caption(resource['description'] + f" | Uploaded on: {resource['dateUploaded']}")

#         # Update resource [Professor 1.4]
#         with col2:
#             if st.button("Edit", key=f"edit_{resource['resourceID']}"):
#                 st.session_state[f'editing_{resource["resourceID"]}'] = True

#         # Delete resource [Professor 1.3] -- FIXED INDENTATION
#         with col3:
#             if st.button("Delete", key=f"delete_{resource['resourceID']}"):
#                 response = requests.delete(f"http://api:4000/cr/resources/{resource['resourceID']}")
#                 if response.status_code == 200:
#                     st.success("Resource deleted successfully!")
#                 else:
#                     st.error("Failed to delete resource.")

#         # Edit form
#         if st.session_state.get(f'editing_{resource["resourceID"]}', False):
#             with st.form(key=f'form_{resource["resourceID"]}'):
#                 new_name = st.text_input("Resource Name", value=resource['name'])
#                 new_description = st.text_area("Description", value=resource['description'])

#                 colA, colB = st.columns(2)
#                 with colA:
#                     if st.form_submit_button("Save Changes"):
#                         update_data = {
#                             "name": new_name,
#                             "description": new_description
#                         }
#                         response = requests.put(f"http://api:4000/cr/resources/{resource['resourceID']}", json=update_data)
#                         if response.status_code == 200:
#                             st.success("Resource updated successfully!")
#                             st.session_state[f'editing_{resource["resourceID"]}'] = False

#                 with colB:
#                     if st.form_submit_button("Cancel"):
#                         st.session_state[f'editing_{resource["resourceID"]}'] = False

#         st.divider()


import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("📚 Course Materials Management")

# Use the hostname from docker-compose.yml
API_BASE_URL = 'http://web-api:4000'

<<<<<<< HEAD
# Select a course from the list of courses retrieved from the API
courses = requests.get('http://api:4000/c/courses').json()
selected_course = st.selectbox(
    "Select a course:",
    courses,
    format_func=lambda x: f"{x['course_name']} CRN: {x['crn']}"
)
st.write(f"You selected: {selected_course['course_name']} (CRN: {selected_course['crn']})")
=======
# Add error handling for connection issues
def make_request(method, endpoint, **kwargs):
    """Helper function to make API requests with error handling"""
    try:
        url = f'{API_BASE_URL}{endpoint}'
        response = requests.request(method, url, timeout=5, **kwargs)
        return response
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Make sure all containers are running.")
        st.stop()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. API might be slow or not responding.")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.stop()
>>>>>>> 374fa3c (update professor-course-mat)

try:
    # Test connection first
    with st.spinner("Connecting to API..."):
        test_response = make_request('GET', '/cr/course')
    
<<<<<<< HEAD
    description = st.text_area("Description")

    if st.button("Upload Resource"):
        data = {
            "resourceID": resource_id,
            "name": resource_name,
            "type": resource_type,
            "dateUploaded": str(upload_date),
            "description": description,
            "CRN": selected_course["crn"]   # FIXED KEY
        }
        response = requests.post('http://api:4000/c/resource', json=data)

        if response.status_code == 201:
            st.success("Resource uploaded successfully!")
        else:
            st.error("Failed to upload resource.")
            st.error(response.json())

st.write("---")

# Manage course materials (update/delete)
st.subheader("Manage Existing Course Materials")
resources = requests.get(f"http://api:4000/c/resources/{selected_course['crn']}").json()

for resource in resources:
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{resource['name']}** ({resource['type']})")
            st.caption(resource['description'] + f" | Uploaded on: {resource['dateUploaded']}")

        # Update resource [Professor 1.4]
        with col2:
            if st.button("Edit", key=f"edit_{resource['resourceID']}"):
                st.session_state[f'editing_{resource["resourceID"]}'] = True

        # Delete resource [Professor 1.3] -- FIXED INDENTATION
        with col3:
            if st.button("Delete", key=f"delete_{resource['resourceID']}"):
                response = requests.delete(f"http://api:4000/c/resource/{resource['resourceID']}")
                if response.status_code == 200:
                    st.success("Resource deleted successfully!")
                else:
                    st.error("Failed to delete resource.")

        # Edit form
        if st.session_state.get(f'editing_{resource["resourceID"]}', False):
            with st.form(key=f'form_{resource["resourceID"]}'):
                new_name = st.text_input("Resource Name", value=resource['name'])
                new_description = st.text_area("Description", value=resource['description'])

                colA, colB = st.columns(2)
                with colA:
                    if st.form_submit_button("Save Changes"):
                        update_data = {
                            "name": new_name,
                            "description": new_description
                        }
                        response = requests.put(f"http://api:4000/c/resource/{resource['resourceID']}", json=update_data)
                        if response.status_code == 200:
                            st.success("Resource updated successfully!")
                            st.session_state[f'editing_{resource["resourceID"]}'] = False

                with colB:
                    if st.form_submit_button("Cancel"):
                        st.session_state[f'editing_{resource["resourceID"]}'] = False

        st.divider()
=======
    if test_response.status_code != 200:
        st.error(f"API Error: {test_response.status_code}")
        st.write(test_response.text)
        st.stop()
    
    courses = test_response.json()
    
    if not courses:
        st.warning("No courses found. Please create a course first.")
        if st.button("Go to Create Course Page"):
            st.switch_page('pages/03_Professor_Manage_Courses.py')
        st.stop()
        
    selected_course = st.selectbox(
        "Select Course", 
        courses, 
        format_func=lambda x: f"{x.get('name', 'Unknown')} (CRN: {x.get('CRN', 'N/A')})"
    )
    
    st.write('---')
    
    # Upload new resource (User Story 1.2 - POST)
    with st.expander("➕ Upload New Resource"):
        with st.form("upload_resource_form"):
            col1, col2 = st.columns(2)
            with col1:
                resource_name = st.text_input("Resource Name*")
                resource_type = st.selectbox("Type*", ["PDF", "Video", "Slides", "Document"])
            with col2:
                resource_id = st.number_input("Resource ID*", min_value=1, value=5001)
                upload_date = st.date_input("Upload Date*")
            
            description = st.text_area("Description*")
            
            submitted = st.form_submit_button("Upload Resource", type="primary")
            
            if submitted:
                if not resource_name or not description:
                    st.error("Please fill in all required fields")
                else:
                    data = {
                        "resourceID": int(resource_id),
                        "name": resource_name,
                        "type": resource_type,
                        "dateUploaded": str(upload_date),
                        "description": description,
                        "CRN": selected_course['CRN']
                    }
                    
                    response = make_request('POST', '/cr/resources', json=data)
                    
                    if response.status_code == 201:
                        st.success("✅ Resource uploaded successfully!")
                        st.rerun()
                    else:
                        error_msg = response.json().get('error', 'Unknown error')
                        st.error(f"❌ Error: {error_msg}")
    
    st.write('---')
    
    # View and manage existing resources
    st.subheader("Existing Resources")
    
    resources_response = make_request('GET', f'/cr/resources?crn={selected_course["CRN"]}')
    
    if resources_response.status_code == 200:
        resources = resources_response.json()
        
        if resources:
            for resource in resources:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{resource.get('name', 'Unnamed')}** ({resource.get('type', 'Unknown')})")
                        st.caption(resource.get('description', 'No description'))
                        st.caption(f"Uploaded: {resource.get('dateUploaded', 'Unknown date')}")
                    
                    # Update resource (User Story 1.4 - PUT)
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{resource['resourceID']}"):
                            st.session_state[f'editing_{resource["resourceID"]}'] = True
                    
                    # Delete resource (User Story 1.3 - DELETE)
                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{resource['resourceID']}", type="secondary"):
                            delete_response = make_request('DELETE', f'/cr/resources/{resource["resourceID"]}')
                            if delete_response.status_code == 200:
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error(f"Error: {delete_response.json().get('error', 'Unknown error')}")
                    
                    # Edit form
                    if st.session_state.get(f'editing_{resource["resourceID"]}', False):
                        with st.form(key=f'form_{resource["resourceID"]}'):
                            new_name = st.text_input("Name", value=resource.get('name', ''))
                            new_type = st.selectbox("Type", ["PDF", "Video", "Slides", "Document"], 
                                                   index=["PDF", "Video", "Slides", "Document"].index(
                                                       resource.get('type', 'PDF')
                                                   ) if resource.get('type') in ["PDF", "Video", "Slides", "Document"] else 0)
                            new_desc = st.text_area("Description", value=resource.get('description', ''))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Save Changes", type="primary"):
                                    update_data = {
                                        "name": new_name, 
                                        "type": new_type,
                                        "description": new_desc
                                    }
                                    update_response = make_request(
                                        'PUT',
                                        f'/cr/resources/{resource["resourceID"]}', 
                                        json=update_data
                                    )
                                    if update_response.status_code == 200:
                                        st.success("Updated!")
                                        st.session_state[f'editing_{resource["resourceID"]}'] = False
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {update_response.json().get('error', 'Unknown error')}")
                            with col2:
                                if st.form_submit_button("Cancel"):
                                    st.session_state[f'editing_{resource["resourceID"]}'] = False
                                    st.rerun()
                    
                    st.divider()
        else:
            st.info("📝 No resources uploaded yet for this course. Use the form above to upload your first resource!")
    else:
        st.error(f"Error loading resources: {resources_response.status_code}")
        
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.write("**Debug info:**")
    st.code(f"API_BASE_URL: {API_BASE_URL}")
>>>>>>> 374fa3c (update professor-course-mat)
