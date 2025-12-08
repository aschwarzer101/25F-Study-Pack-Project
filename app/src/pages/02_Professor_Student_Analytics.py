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

st.header('Student Analytics Dashboard') 

courses = requests.get('http://web-api:4000/c/courses').json()
selected_course = st.selectbox("Select a course to view analytics:", courses, format_func = lambda x: f"{x['course_name']} CRN: {x['crn']}")

st.write("---")

# See topics students are working on [Professor-6]
st.subheader("Topics Students are Working On")
topics_response = requests.get(
    f"http://web-api:4000/s/study_time/professor/{st.session_state['professor_id']}/topics"
)
study_time_data = topics_response.json()

if study_time_data:
    df_study = pd.DataFrame(study_time_data)

    fig = px.bar(df_study, x = 'Topic', y = 'Total_Study_Time',
    title = f"Total Study Time by Topic for {selected_course['course_name']}",
    labels = {'Total_Study_Time': 'Total Study Time (minutes)', 'Topic': 'Topic'})
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_study, use_container_width=True)

st.subheader("Session Details")
selected_topic = st.selectbox("View sessions for topic:", df_study['Topic'].tolist())

sessions = requests.get(f'http://web-api:4000/s/sessions/topic/{selected_topic}').json()

for session in sessions:
    with st.expander(f"Session {session['sessionID']} - {session['date']}"):
            session_details = requests.get(f'http://web-api:4000/s/study_session/{session["sessionID"]}').json()
            st.json(session_details)
else:
    st.info("No study session data available yet")
