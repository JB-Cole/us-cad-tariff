#data.py

import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📂 Data Files")

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

csv_files = sorted(data_folder.glob("*.csv"))
if not csv_files:
    st.info("No data CSVs found. Please Fetch on the Trends page first.")
else:
    for csv_path in csv_files:
        st.subheader(csv_path.name)
        df = pd.read_csv(csv_path, parse_dates=["Reference period"])
        st.dataframe(df)
        st.download_button(
            label=f"Download {csv_path.name}",
            data=df.to_csv(index=False),
            file_name=csv_path.name,
            mime="text/csv"
        )
