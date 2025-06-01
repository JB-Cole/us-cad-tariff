import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os

# Set page configuration
st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')

# Function to load Lottie animation from URL or local file
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # Raise an exception for bad status codes
        print(f"Response status code: {r.status_code}")
        print(f"Response content (first 100 chars): {r.text[:100]}...")  # Debug content
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to load URL {url}: {e}")
        return None
    except ValueError as e:
        print(f"Invalid JSON from {url}: {e}")
        return None

# Animation URL (replace with the actual JSON URL or use local file)
animation_url = "https://lottie.host/embed/ee902cb7-8ee2-4492-8803-04ab8af79912/ES0VAvDI6q.json"  # Adjust this URL
local_animation_path = "construction_animation.json"  # Path to local JSON file if downloaded

# Load animation (prefer local file if URL fails)
animation = None
if os.path.exists(local_animation_path):
    with open(local_animation_path, "r") as f:
        animation = f.read()
    print(f"Loaded animation from local file: {local_animation_path}")
else:
    animation = load_lottie_url(animation_url)

# CSS to style the animation as a header
st.markdown(
    """
    <style>
    .header-container {
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px 0;
        border-bottom: 2px solid #d3d3d3;
        margin-bottom: 20px;
    }
    .lottie-animation {
        display: inline-block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display animation as header
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if animation:
    st_lottie(
        animation,
        height=200,
        width=400,
        key="header-animation",
        speed=1,
        loop=True,
        quality="high",
        element_attr={"class": "lottie-animation"}
    )
else:
    st.error("Animation failed to load. Please check the URL or download the JSON file.")
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