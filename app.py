import streamlit as st

st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')

# Clear cache when the app loads
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared successfully!")

st.title('🏗️ U.S. - Canada Tariff Impact on Construction and Production sectors')
st.markdown("""
Welcome to an interactive dashboard for exploring the impact of U.S. - Canada tariffs on Canada's production and construction sectors.

On the Trends page, you will find a button to retrieve IPPI data for Fabricated metal products and construction materials [P63] and RMPI for Metal ores, concentrates and scrap [M61] both from Statistics Canada.

You can filter these indeces by date to highlight two key phases of the tariff dispute: the tariff implementation (January 2025) and the subsequent lobbying period (March 2025). 

Since StatCan updates its data quarterly, the most recent figures extend through April 2025, and you can visualize indices dating back to 2020. All StatCan data is scraped and saved as CSV files in the Data tab.

Use the sidebar to switch between pages:
- Data 
- Trends (IPPI vs RMPI)


For more deatils on this project, Visit GitHub Repo.
""")