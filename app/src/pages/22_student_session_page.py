import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Available Study Sessions')

st.write('\n\n')
st.write('## Model 1 Maintenance')

st.write("## Search Predictions")
search_value = st.text_input("Enter two numbers (format: x,y):", "")

if st.button("Search Prediction", type="primary", use_container_width=True):
    try:
        x, y = search_value.split(",")
        url = f"http://web-api:4000/prediction/{x.strip()}/{y.strip()}"
        results = requests.get(url).json()
        st.success("Prediction retrieved!")
        st.dataframe(results)
    except:
        st.error("Please enter values correctly, like `10, 25`.")

# -------------------------
# 🗺️ Add Interactive Map
# -------------------------
st.write("## Interactive Map of Predictions")

# Example: converting API results into coordinates
# Modify depending on your API output format
if st.checkbox("Show Prediction Map"):
    try:
        # Sample: Get a grid of predictions for mapping
        map_data = []
        for i in range(5, 30, 5):
            for j in range(5, 30, 5):
                url = f"http://web-api:4000/prediction/{i}/{j}"
                res = requests.get(url).json()
                # Expect your API returns something like { "prediction": number }
                map_data.append({
                    "lat": float(i), 
                    "lon": float(j),
                    "value": float(res.get("prediction", 0))
                })

        df = pd.DataFrame(map_data)
        st.map(df, latitude="lat", longitude="lon")
        st.write("Prediction Values Shown on Map:")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error loading map data: {e}")

