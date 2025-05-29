import streamlit as st
from scraper.statcan_scraper import IndexTracker
import pandas as pd
from streamlit_echarts import st_echarts

st.set_page_config(page_title="IPPI vs RMPI Trends", layout="wide")

st.title("📊 IPPI vs RMPI Trends")
st.markdown("Analyze the monthly changes in Industrial Product Price Index (IPPI) and Raw Material Price Index (RMPI) from Statistics Canada. For broader context, select Start date as 2024/01/01 and current date as End date. Scraper code is updated as and when new information is available on Statistics Canada")

# Initialize session state for data
if 'ippi_data' not in st.session_state:
    st.session_state.ippi_data = None
if 'rmpi_data' not in st.session_state:
    st.session_state.rmpi_data = None

# Date range selectors
min_date = pd.Timestamp("2020-01-01")
max_date = pd.Timestamp.today()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Define the two index trackers
ippi_tracker = IndexTracker(
    index_name="IPPI",
    page_url="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026501&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2024&cubeTimeFrame.endMonth=04&cubeTimeFrame.endYear=2025&referencePeriods=20240101%2C20250401",
    target_product="Fabricated metal products and construction materials [P63]"
)

rmpi_tracker = IndexTracker(
    index_name="RMPI",
    page_url="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026801&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2024&cubeTimeFrame.endMonth=05&cubeTimeFrame.endYear=2025&referencePeriods=20240101%2C20250501",
    target_product="Metal ores, concentrates and scrap [M61]"
)

# Scraping buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Fetch IPPI Data"):
        with st.spinner("Fetching IPPI data..."):
            st.session_state.ippi_data = ippi_tracker.fetch_data()
            st.success("IPPI data fetched!")
            st.dataframe(st.session_state.ippi_data)

with col2:
    if st.button("🔄 Fetch RMPI Data"):
        with st.spinner("Fetching RMPI data..."):
            st.session_state.rmpi_data = rmpi_tracker.fetch_data()
            st.success("RMPI data fetched!")
            st.dataframe(st.session_state.rmpi_data)

# Show chart only when user clicks 'Generate Graph' and both datasets exist
if st.session_state.ippi_data is not None and st.session_state.rmpi_data is not None:
    if st.button("📈 Generate Comparison Graph"):
        merged = pd.merge(
            st.session_state.ippi_data,
            st.session_state.rmpi_data,
            on='Reference period',
            suffixes=('_IPPI', '_RMPI')
        )

        merged = merged[(merged['Reference period'] >= pd.to_datetime(start_date)) &
                        (merged['Reference period'] <= pd.to_datetime(end_date))]

        merged.sort_values('Reference period', inplace=True)

        x_data = merged['Reference period'].dt.strftime("%b %Y").tolist()

        options = {
            "backgroundColor": "#B6B4B4",
            "title": {"text": "IPPI vs RMPI Over Time", "textStyle": {"color": "#ffffff"}},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["IPPI", "RMPI"], "textStyle": {"color": "#ffffff"}},
            "xAxis": {
                "type": "category",
                "data": x_data,
                "axisLabel": {"rotate": 45, "color": "#ffffff"},
                "axisPointer": {"type": "shadow"}
            },
            "yAxis": {"type": "value", "axisLabel": {"color": "#ffffff"}},
            "series": [
                {
                    "name": "IPPI",
                    "type": "line",
                    "data": merged['Value_IPPI'].tolist(),
                    "smooth": True,
                    "itemStyle": {"color": "#12170F"},
                    "markLine": {
                        "data": [
                            {"xAxis": "Jan 2025", "label": {"formatter": "Tariff Start"}},
                            {"xAxis": "Mar 2025", "label": {"formatter": "Lobbying"}}
                        ],
                        "lineStyle": {"type": "dashed", "color": "#6B4E37"},
                        "label": {"color": "#ffffff", "fontWeight": "bold"}
                    }
                },
                {
                    "name": "RMPI",
                    "type": "line",
                    "data": merged['Value_RMPI'].tolist(),
                    "smooth": True,
                    "itemStyle": {"color": "#174F17"}
                }
            ],
            "dataZoom": [{"type": "inside"}, {"type": "slider"}]
        }

        st_echarts(options=options, height="550px")
else:
    st.info("Please fetch both IPPI and RMPI datasets, then click 'Generate Comparison Graph' to view the chart.")