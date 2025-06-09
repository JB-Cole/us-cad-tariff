import streamlit as st

st.set_page_config(page_title='Tariff Impact on Construction', layout='wide')


st.title('🏗️ U.S. - Canada Tariff Impact on Construction and Production sectors')

st.markdown("""
# Welcome to an interactive dashboard for exploring the impact of U.S. - Canada tariffs on Canada's production and construction sectors.

### Background
The Canadian construction industry is facing significant challenges due to recent trade tensions and retaliatory tariffs between Canada and the United States. A 25% tariff imposed by the U.S. on Canadian construction materials, including steel and aluminum, has triggered rising costs, supply chain disruptions, and affordability issues in both countries.

### Data Source
This app utilizes web scraping to retrieve the following data from Statistics Canada:
- **Raw Materials Price Indices (RMPI)** for Metal ores, concentrates and scrap [M61]
- **Industrial Product Price Index (IPPI)** for Fabricated metal products and construction materials [P63]

### Visualization
Visualize trends using line plots that highlight two key phases of the tariff dispute:
- The tariff implementation (January 2025)
- The subsequent lobbying period (March 2025)

The retrieved data is stored in CSV files, available for download on the **Data** page.

### Navigation
Use the sidebar to switch between pages:
- **Data**
- **Trends (IPPI vs RMPI)**

### How to Use the App
1. **Clear Cache**: Click the "Clear Cache" button before retrieving data and generating the graph to ensure fresh data.
2. **Select Date Range**: Choose a date range between January 2020 and April 2025 (the most recent date for data on StatCan) for your start and end dates.
3. **Fetch Data**: Click "Fetch IPPI" and "Fetch RMPI" to retrieve the data.
4. **Generate Graph**: Click "Generate Comparison Graph" to visualize the data.


### Additional Information
For details on updating code for other IPPIs vs RMPIs visualizations, visit the [GitHub Repo](https://github.com/JB-Cole/us-cad-tariff/blob/main/CONTRIBUTING.md).
""")

# Clear cache when the app loads
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared successfully!")