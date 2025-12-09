import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Student Home Page')

if st.button('Find a study session', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_student_session_page.py')

if st.button('Find a course', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_student_courses_page.py')

if st.button('Find a tutor', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_find_tutors.py')