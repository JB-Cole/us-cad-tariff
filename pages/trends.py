import streamlit as st
from scraper.statcan_scraper import IndexTracker
import pandas as pd
from streamlit_echarts import st_echarts

st.set_page_config(page_title="IPPI vs RMPI Trends", layout="wide")

st.title("📊 IPPI vs RMPI Trends (CSV-Based)")
st.markdown("Analyze the monthly changes in Industrial Product Price Index (IPPI) and Raw Material Price Index (RMPI) using direct CSV downloads from Statistics Canada.")

# Initialize session state for data caching
if 'ippi_df' not in st.session_state:
    st.session_state.ippi_df = None
if 'rmpi_df' not in st.session_state:
    st.session_state.rmpi_df = None

# Date range selectors
min_date = pd.Timestamp("2020-01-01")
max_date = pd.Timestamp.today()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Define the two index trackers using table PIDs
ippi_tracker = IndexTracker(
    index_name="IPPI",
    pid="1810026501",
    target_product="Fabricated metal products and construction materials [P63]"
)

rmpi_tracker = IndexTracker(
    index_name="RMPI",
    pid="1810026801",
    target_product="Metal ores, concentrates and scrap [M61]"
)

# Fetch data buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Fetch IPPI Data"):
        with st.spinner("Downloading IPPI CSV..."):
            st.session_state.ippi_df = ippi_tracker.fetch_data()
            st.success("IPPI data ready!")
            st.dataframe(st.session_state.ippi_df)
with col2:
    if st.button("🔄 Fetch RMPI Data"):
        with st.spinner("Downloading RMPI CSV..."):
            st.session_state.rmpi_df = rmpi_tracker.fetch_data()
            st.success("RMPI data ready!")
            st.dataframe(st.session_state.rmpi_df)

# Generate and display the chart
if st.session_state.ippi_df is not None and st.session_state.rmpi_df is not None:
    if st.button("📈 Generate Comparison Graph"):
        # Merge on reference period
        df_ipp = st.session_state.ippi_df
        df_rmp = st.session_state.rmpi_df
        merged = pd.merge(df_ipp, df_rmp, on='Reference period', suffixes=('_IPPI','_RMPI'))
        # Filter by selected date range
        merged = merged[(merged['Reference period'] >= pd.to_datetime(start_date)) &
                        (merged['Reference period'] <= pd.to_datetime(end_date))]
        merged.sort_values('Reference period', inplace=True)

        x_data = merged['Reference period'].dt.strftime("%b %Y").tolist()

        options = {
            "backgroundColor": "#646262",
            "title": {"text": "IPPI vs RMPI Over Time", "textStyle": {"color": "#ffffff"}},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["IPPI","RMPI"], "textStyle": {"color": "#ffffff"}},
            "xAxis": {"type": "category", "data": x_data, "axisLabel": {"rotate":45, "color":"#ffffff"}},
            "yAxis": {"type": "value", "axisLabel": {"color":"#ffffff"}},
            "series": [
                {
                    "name": "IPPI",
                    "type": "line",
                    "data": merged['Value_IPPI'].tolist(),
                    "smooth": True,
                    "itemStyle": {"color": "#000000"},
                    "markLine": {
                        "data": [
                            {"xAxis": "Jan 2025", "label": {"formatter": "Tariff Start", "color":"#ffffff"}},
                            {"xAxis": "Mar 2025", "label": {"formatter": "Lobbying", "color":"#ffffff"}}
                        ],
                        "lineStyle": {"type": "dashed", "color": "#403024"}
                    }
                },
                {
                    "name": "RMPI",
                    "type": "line",
                    "data": merged['Value_RMPI'].tolist(),
                    "smooth": True,
                    "itemStyle": {"color": "#0A230A"}
                }
            ],
            "markArea": {
                "data": [
                    [
                        {"xAxis": "Jan 2025"}, {"xAxis": "Feb 2025"}
                    ],
                    [
                        {"xAxis": "Mar 2025"}, {"xAxis": "Apr 2025"}
                    ]
                ],
                "itemStyle": {"color": "#a9a9a9"},
                "silent": True
            },
            "markArea2": {
                "data": [
                    [
                        {"xAxis": "Mar 2025"}, {"xAxis": "Apr 2025"}
                    ]
                ],
                "itemStyle": {"color": "#8b4513"},
                "silent": True
            },
            "dataZoom": [{"type": "inside"}, {"type": "slider"}]
        }

        st_echarts(options=options, height="550px")
else:
    st.info("Fetch both IPPI & RMPI data, then click ‘Generate Comparison Graph’.")
