import streamlit as st
import pandas as pd
from scraper.statcan_scraper import IndexTracker
from streamlit_echarts import st_echarts
    

# Page Setup
st.set_page_config(page_title="IPPI vs RMPI Trends", layout="wide")
st.title("IPPI vs RMPI Trends")
st.markdown("Select date range. Fetch Data to Generate Graphs.")

# Date input
min_date = pd.Timestamp("2020-01-01")
max_date = pd.Timestamp.today()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Initialize session state for data
if 'df_ip' not in st.session_state:
    st.session_state['df_ip'] = pd.DataFrame()
if 'df_rm' not in st.session_state:
    st.session_state['df_rm'] = pd.DataFrame()

# IndexTracker instances
ippi = IndexTracker(pid="1810026501", target_product="v1230995999")
rmpi = IndexTracker(pid="1810026801", target_product="v1230998193")

# Fetch Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Fetch IPPI"):
        try:
            df_ip = ippi.fetch_data(start=start_date, end=end_date)
            if df_ip.empty:
                st.error("No IPPI data fetched. Check date range or target product.")
            else:
                st.session_state['df_ip'] = df_ip
                st.success(f"Fetched IPPI data with {len(df_ip)} rows")
                st.dataframe(df_ip)
        except Exception as e:
            st.error(f"Failed to fetch IPPI: {e}")

with col2:
    if st.button("Fetch RMPI"):
        try:
            df_rm = rmpi.fetch_data(start=start_date, end=end_date)
            if df_rm.empty:
                st.error("No RMPI data fetched. Check date range or target product.")
            else:
                st.session_state['df_rm'] = df_rm
                st.success(f"Fetched RMPI data with {len(df_rm)} rows")
                st.dataframe(df_rm)
        except Exception as e:
            st.error(f"Failed to fetch RMPI: {e}")


# Load data from session state
df_ip = st.session_state['df_ip']
df_rm = st.session_state['df_rm']

# Validate
if df_ip.empty or df_rm.empty:
    st.warning("Both IPPI and RMPI data must be available.")
    st.stop()

# Rename columns
df_ip = df_ip[["Reference period", "Value"]].rename(columns={"Value": "IPPI"})
df_rm = df_rm[["Reference period", "Value"]].rename(columns={"Value": "RMPI"})

# Merge on Reference period
merged = pd.merge(df_ip, df_rm, on="Reference period", how="inner")
merged = merged[(merged["Reference period"] >= start_date) & (merged["Reference period"] <= end_date)].dropna()

if merged.empty:
    st.error("No overlapping data in selected date range.")
    st.stop()

# Generate Comparison Chart
if st.button("Generate Comparison Graph"):
    x_data = merged["Reference period"].dt.strftime("%b %Y").tolist()

    options = {
        "backgroundColor": "#FFFFFFFF",
        "title": {"text": "IPPI vs RMPI Over Time", "textStyle": {"color": "#000000"}},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["IPPI", "RMPI"], "textStyle": {"color": "#000000"}},
        "xAxis": {
            "type": "category",
            "data": x_data,
            "axisLabel": {"rotate": 45, "color": "#000000"},
            "axisPointer": {"type": "shadow"}
        },
        "yAxis": {"type": "value", "axisLabel": {"color": "#000000"}},
        "series": [
            {
                "name": "IPPI",
                "type": "line",
                "data": merged['IPPI'].tolist(),
                "smooth": True,
                "itemStyle": {"color": "#23558E"},
                "markLine": {
                    "data": [
                        {"xAxis": "Jan 2025", "label": {"formatter": "Tariff Start"}},
                        {"xAxis": "Mar 2025", "label": {"formatter": "Lobbying"}}
                    ],
                    "lineStyle": {"type": "dashed", "color": "#FF0000"},
                    "label": {"color": "#000000", "fontWeight": "bold"}
                }
            },
            {
                "name": "RMPI",
                "type": "line",
                "data": merged['RMPI'].tolist(),
                "smooth": True,
                "itemStyle": {"color": "#174F17"}
            }
        ],
        "dataZoom": [{"type": "inside"}, {"type": "slider"}]
    }
    st_echarts(options=options, height="550px")

# Rolling Correlation Section
st.markdown("---")
st.header("Rolling Correlation Between IPPI and RMPI")

# Rolling window slider
window_size = st.slider("Rolling Window Size (months)", min_value=3, max_value=12, value=6)

# Calculate rolling correlation
merged["rolling_corr"] = merged["IPPI"].rolling(window=window_size).corr(merged["RMPI"])
rolling_df = merged[["Reference period", "rolling_corr"]].dropna()

# Visualize
st.subheader(f"Rolling Correlation ({window_size}-month window)")
st.line_chart(rolling_df.set_index("Reference period"))
