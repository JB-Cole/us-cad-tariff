import streamlit as st
import pandas as pd
from scraper.bcpi_scraper import BCPITracker
from streamlit_echarts import st_echarts
from db_utils import create_db_engine, save_table, query_table

# Auth check
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.error("Please log in on the home page to access this content.")
    st.markdown("[Go to Home Page](/)")
    st.stop()

# Page Setup
st.set_page_config(page_title="BCPI Trends", layout="wide")
st.title("BCPI Trends for Residential and Non-Residential buildings in Canada, Divison: Metal fabrications")
st.markdown("Select date range. Fetch & save to DB, then generate graphs.")

# Date input
min_date = pd.Timestamp("2020-01-01")
max_date = pd.Timestamp.today()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# DB connection
engine = create_db_engine(
    user='postgres',
    password='1234',
    host='localhost',
    database='tariffdb'
)

# Tracker instances
res_bcpi = BCPITracker(pid="1810028901", target_vectors=["v1617908010"])
nonres_bcpi = BCPITracker(pid="1810028901", target_vectors=["v1617908154"])

# Fetch Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Fetch Residential BCPI"):
        try:
            df_res = res_bcpi.fetch_data(start_quarter=start_date.to_period("Q").strftime("%YQ%q"),
                                         end_quarter=end_date.to_period("Q").strftime("%YQ%q"))
            if df_res.empty:
                st.error("No Residential BCPI data fetched. Check date range.")
            else:
                save_table(df_res, 'bcpi_residential', engine, mode='replace')
                st.success(f"Saved Residential BCPI to DB with {len(df_res)} rows")
                st.dataframe(df_res)
        except Exception as e:
            st.error(f"Failed to fetch Residential BCPI: {e}")

with col2:
    if st.button("Fetch Non-Residential BCPI"):
        try:
            df_nonres = nonres_bcpi.fetch_data(start_quarter=start_date.to_period("Q").strftime("%YQ%q"),
                                               end_quarter=end_date.to_period("Q").strftime("%YQ%q"))
            if df_nonres.empty:
                st.error("No Non-Residential BCPI data fetched. Check date range.")
            else:
                save_table(df_nonres, 'bcpi_nonresidential', engine, mode='replace')
                st.success(f"Saved Non-Residential BCPI to DB with {len(df_nonres)} rows")
                st.dataframe(df_nonres)
        except Exception as e:
            st.error(f"Failed to fetch Non-Residential BCPI: {e}")

# Load from DB
df_res = query_table(engine, "SELECT * FROM bcpi_residential")
df_nonres = query_table(engine, "SELECT * FROM bcpi_nonresidential")

# Validate
if df_res.empty or df_nonres.empty:
    st.warning("Both Residential and Non-Residential BCPI data must be available.")
    st.stop()

# Prepare data
df_res = df_res[["REF_DATE", "VALUE"]].rename(columns={"VALUE": "Residential"})
df_res["REF_DATE"] = pd.to_datetime(df_res["REF_DATE"])
df_nonres = df_nonres[["REF_DATE", "VALUE"]].rename(columns={"VALUE": "Non-Residential"})
df_nonres["REF_DATE"] = pd.to_datetime(df_nonres["REF_DATE"])

# Merge datasets
merged = pd.merge(df_res, df_nonres, on="REF_DATE", how="inner")
merged = merged[(merged["REF_DATE"] >= start_date) & (merged["REF_DATE"] <= end_date)].dropna()

if merged.empty:
    st.error("No overlapping BCPI data in selected date range.")
    st.stop()

# Generate Residential BCPI Chart
if st.button("Generate Residential BCPI Graph"):
    x_data_res = merged["REF_DATE"].dt.strftime("%Y-Q%q").tolist()
    options_res = {
        "backgroundColor": "#FFFFFFFF",
        "title": {"text": "BCPI: Residential Buildings", "textStyle": {"color": "#000000"}},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Residential"], "textStyle": {"color": "#000000"}},
        "xAxis": {
            "type": "category",
            "data": x_data_res,
            "axisLabel": {"rotate": 45, "color": "#000000"},
            "axisPointer": {"type": "shadow"}
        },
        "yAxis": {"type": "value", "axisLabel": {"color": "#000000"}},
        "series": [
            {
                "name": "Residential",
                "type": "line",
                "data": merged['Residential'].tolist(),
                "smooth": True,
                "itemStyle": {"color": "#23558E"}
            }
        ],
        "dataZoom": [{"type": "inside"}, {"type": "slider"}]
    }
    st_echarts(options=options_res, height="450px")

# Generate Non-Residential BCPI Chart
if st.button("Generate Non-Residential BCPI Graph"):
    x_data_nonres = merged["REF_DATE"].dt.strftime("%Y-Q%q").tolist()
    options_nonres = {
        "backgroundColor": "#FFFFFFFF",
        "title": {"text": "BCPI: Non-Residential Buildings", "textStyle": {"color": "#000000"}},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Non-Residential"], "textStyle": {"color": "#000000"}},
        "xAxis": {
            "type": "category",
            "data": x_data_nonres,
            "axisLabel": {"rotate": 45, "color": "#000000"},
            "axisPointer": {"type": "shadow"}
        },
        "yAxis": {"type": "value", "axisLabel": {"color": "#000000"}},
        "series": [
            {
                "name": "Non-Residential",
                "type": "line",
                "data": merged['Non-Residential'].tolist(),
                "smooth": True,
                "itemStyle": {"color": "#174F17"}
            }
        ],
        "dataZoom": [{"type": "inside"}, {"type": "slider"}]
    }
    st_echarts(options=options_nonres, height="450px")
