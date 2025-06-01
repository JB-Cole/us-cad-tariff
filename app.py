import streamlit as st

st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')

st.title('🏗️ Construction Tariff Impact Dashboard')
st.markdown("""
Welcome to our interactive dashboard for exploring the impact of U.S. - Canada tariffs on Canada's production and construction sectors. On the Trends page, you can filter index data to highlight two key phases of the tariff dispute: the tariff implementation (January 2025) and the subsequent lobbying period (March 2025). Since StatCan updates its data quarterly, the most recent figures extend through May 2025, and you can visualize indices dating back to 2020. All StatCan data is scraped and saved as CSV files in the Data tab.

Use the sidebar to switch between pages:
- Data 
- Trends (IPPI vs RMPI)


For more deatils on this project, Visit GitHub Repo.
""")
