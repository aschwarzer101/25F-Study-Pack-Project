import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Student Homepage!')

# user story 1
if st.button('Find a study session', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_student_session_page.py')

# user story 2
if st.button('Search for courses', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_student_courses_page.py')

# user story 3
if st.button('Find a tutor', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_ML_Model_Mgmt.py')