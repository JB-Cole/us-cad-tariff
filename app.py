import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os

# Set page configuration
st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')

# Function to load Lottie animation from local file
local_animation_path = "construction_animation.json"  # Path to local JSON file

# Load animation
animation = None
if os.path.exists(local_animation_path):
    with open(local_animation_path, "r") as f:
        animation = f.read()
    print(f"Loaded animation from local file: {local_animation_path}")
else:
    st.error("Local animation file not found. Please ensure 'construction_animation.json' is in the project directory.")

# CSS to center the animation at the top
st.markdown(
    """
    <style>
    .animation-container {
        text-align: center;
        margin-bottom: 20px;  /* Space between animation and title */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display animation at the top
st.markdown('<div class="animation-container">', unsafe_allow_html=True)
if animation:
    st_lottie(
        animation,
        height=200,
        width=400,
        key="top-animation",
        speed=1,
        loop=True,
        quality="high"
    )
else:
    st.error("Animation failed to load.")
st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title('🏗️ Construction Tariff Impact Dashboard')
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    Welcome to our interactive dashboard for exploring the impact of U.S. - Canada tariffs on Canada's production and construction sectors. On the Trends page, you can filter index data to highlight two key phases of the tariff dispute: the tariff implementation (January 2025) and the subsequent lobbying period (March 2025). Since StatCan updates its data quarterly, the most recent figures extend through May 2025, and you can visualize indices dating back to 2020. All StatCan data is scraped and saved as CSV files in the Data tab.

    Use the sidebar to switch between pages:
    - Data 
    - 📊 Trends (IPPI vs RMPI)
    """)

with col2:
    st.write("")  # Placeholder to balance columns

st.markdown("""
For more details on this project, visit the [GitHub Repo](#).
""", unsafe_allow_html=True)