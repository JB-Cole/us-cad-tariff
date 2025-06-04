# trends.py
import streamlit as st
import pandas as pd
from pathlib import Path
from scraper.statcan_scraper import IndexTracker
from streamlit_echarts import st_echarts

# Page & Data Setup
st.set_page_config(page_title="IPPI vs RMPI Trends", layout="wide")
st.title("📊 IPPI vs RMPI Trends")
st.markdown("Select date range. Fetch to pull & filter CSV, then Generate Graph.")

# Ensure data directory exists
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Date Pickers
min_date = pd.Timestamp("2020-01-01")
max_date = pd.Timestamp.today()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
start_date = pd.to_datetime(min_date)
end_date = pd.to_datetime(max_date)

# CSV-Only Trackers 
ippi = IndexTracker(
    pid="1810026501",
    target_product="v1230995999"
)
rmpi = IndexTracker(
    pid="1810026801",
    target_product="v1230998193"
)

# Fetch & Save Buttons 
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Fetch IPPI"):
        try:
            df_ip = ippi.fetch_data(start=start_date, end=end_date)
            if df_ip.empty:
                st.error("No IPPI data fetched. Check date range or target product.")
            else:
                df_ip.to_csv(data_dir/"ippi.csv", index=False)
                # Verify file was written
                if (data_dir/"ippi.csv").exists():
                    written_df = pd.read_csv(data_dir/"ippi.csv")
                    st.success(f"✅ Fetched & saved data/ippi.csv with {len(written_df)} rows")
                    st.dataframe(df_ip)
                else:
                    st.error("Failed to save IPPI CSV.")
        except Exception as e:
            st.error(f"Failed to fetch IPPI: {e}")

with col2:
    if st.button("🔄 Fetch RMPI"):
        try:
            df_rm = rmpi.fetch_data(start=start_date, end=end_date)
            if df_rm.empty:
                st.error("No RMPI data fetched. Check date range or target product.")
            else:
                df_rm.to_csv(data_dir/"rmpi.csv", index=False)
                # Verify file was written
                if (data_dir/"rmpi.csv").exists():
                    written_df = pd.read_csv(data_dir/"rmpi.csv")
                    st.success(f"✅ Fetched & saved data/rmpi.csv with {len(written_df)} rows")
                    st.dataframe(df_rm)
                else:
                    st.error("Failed to save RMPI CSV.")
        except Exception as e:
            st.error(f"Failed to fetch RMPI: {e}")

# Helper to Load Saved CSVs
@st.cache_data
def load_csv(fname: str, _cache_buster: str = "") -> pd.DataFrame:
    path = data_dir / fname
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, parse_dates=["Reference period"])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    return df

# Invalidate cache when new data is fetched
cache_buster = str(start_date) + str(end_date)

# Require both files before continuing
if not (data_dir/"ippi.csv").exists() or not (data_dir/"rmpi.csv").exists():
    st.info("🔎 Please Fetch both datasets above.")
    st.stop()

# Load CSVs
df_ip = load_csv("ippi.csv", cache_buster)
if df_ip.empty:
    st.warning("⚠️ The IPPI CSV is empty. Try a different date range and Fetch again.")
    st.stop()

df_rm = load_csv("rmpi.csv", cache_buster)
if df_rm.empty:
    st.warning("⚠️ The RMPI CSV is empty. Try a different date range and Fetch again.")
    st.stop()

# ECharts Comparison Graph
if st.button("📈 Generate Comparison Graph"):
    merged = pd.merge(
        df_ip, df_rm,
        on="Reference period",
        suffixes=("_IPPI", "_RMPI")
    )
    merged = merged[(merged['Reference period'] >= pd.to_datetime(start_date)) &
                        (merged['Reference period'] <= pd.to_datetime(end_date))]

    merged.sort_values('Reference period', inplace=True)

    x_data = merged['Reference period'].dt.strftime("%b %Y").tolist()

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
                "data": merged['Value_IPPI'].tolist(),
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
                "data": merged['Value_RMPI'].tolist(),
                "smooth": True,
                "itemStyle": {"color": "#174F17"}
            }
        ],
        "dataZoom": [{"type": "inside"}, {"type": "slider"}]
    }
    st_echarts(options=options, height="550px")