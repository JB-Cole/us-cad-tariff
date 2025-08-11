import pandas as pd
import streamlit as st
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader

# Version Check
print(pd.__version__)
assert hasattr(pd, 'DataFrame'), "pandas.DataFrame is missing!"

# Page Setup
st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')

# Initialize Session State
# if 'authentication_status' not in st.session_state:
#     st.session_state['authentication_status'] = None
#     st.session_state['name'] = None
#     st.session_state['username'] = None

# # Load Authenticator Configuration
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# Debugging
#st.write("Loaded config:", config)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

# # Perform Login
# try:
#     login_result = authenticator.login(fields={'Form name': 'Login'}, location='main')
# except Exception as e:
#     st.error(f"Login crashed: {e}")
#     st.stop()

# if login_result is not None:
#     name, authentication_status, username = login_result
# else:
#     st.error("Login failed due to an internal issue.")
#     st.stop()

# # Handle Login Outcome
# if authentication_status is False:
#     st.error('Username/password is incorrect')
#     st.stop()
# elif authentication_status is None:
#     st.warning('Please enter your username(admin) and password(ADMIN)')
#     st.stop()
# else:
#     st.session_state['authentication_status'] = True
#     st.session_state['name'] = name
#     st.session_state['username'] = username

# # Authenticated App Content
# if st.session_state['authentication_status']:

#     # Sidebar
#     with st.sidebar:
#         authenticator.logout('Logout', 'sidebar')
  

    # Main Dashboard
st.title('U.S. - Canada Tariff Impact on Construction and Production sectors')

st.markdown("""
    ### Welcome to an interactive dashboard for exploring the impact of U.S. - Canada tariffs on Canada's production and construction sectors.

    ### Background
    The Canadian Construction and Production industry is facing significant challenges due to recent trade tensions and retaliatory tariffs between Canada and the United States. 
    In response to the U.S. tariffs on aluminum and steel, Canada has introduced tariffs on an additional 29.8 billion dollars worth of U.S. products (on top of the pre-existing 30 billion dollars worth of goods). 
    For more details, visit [Canada vs U.S.](https://www.cfib-fcei.ca/en/site/us-tariffs#:~:text=Canada%20has%20imposed%20a%2025,billion%20worth%20of%20U.S.%20goods.&text=In%20response%20to%20the%20U.S.,%2430%20billion%20worth%20of%20goods)

    ### Data Source
    This app utilizes web scraping to retrieve the following data from Statistics Canada:
    - **Raw Materials Price Indices (RMPI)** for Metal ores, concentrates and scrap [M61]
    - **Industrial Product Price Index (IPPI)** for Fabricated metal products and construction materials [P63]
    - **Building Construction Price Index (BCPI)** for residential and non-residential buildings in canada, in the metal fabrications division.

    ### Visualization
    Visualize trends using line plots that highlight two key phases of the tariff dispute:
    - The tariff implementation (January 2025)
    - The subsequent lobbying period (March 2025)

    The retrieved data is stored in CSV files, available for download on the **Data** page.

    ### Navigation
    Use the sidebar to switch between pages:
    - **Data**
    - **Trends (IPPI vs RMPI)**
    - **Trends (BCPI)**

    ### How to Use the App
    1. **Select Date Range**: Choose a date range between January 2020 and the current date for start and end dates.(the most recent data from Statcan is retrieved)
    2. **Fetch Data**: Click "Fetch IPPI" and "Fetch RMPI" to retrieve the data.
    3. **Generate Graph**: Click "Generate Comparison Graph" to visualize the data.
    4. **Select Date Range**: Choose a date range between January 2020 and the current date for start and end dates.(the most recent data from Statcan is retrieved)
    5. **Fetch Data**: Click "Fetch residnetial BCPI" and "Fetch non-residnetial BCPI" to retrieve the data.
    6. **Generate Graph**: Click "Generate residential BCPI Graph" or "Generate non-residential BCPI Graph"  to visualize the data.
    7. **View and Download retrieved Data**: Use the Data tab to view the retrieved data and download as csv files.
    """)

    
    





# import bcrypt
# password = "ADMIN".encode('utf-8')
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# print(hashed.decode('utf-8'))
