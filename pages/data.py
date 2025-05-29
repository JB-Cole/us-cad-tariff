import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📂 Data Files")

data_folder = Path("data")
csv_files = sorted(data_folder.glob("*.csv"))

if not csv_files:
    st.info("No data CSVs found. Fetch data from the Trends page first.")
else:
    for csv in csv_files:
        st.subheader(csv.name)
        df = pd.read_csv(csv)
        st.dataframe(df)
        st.download_button(
            label="Download " + csv.name,
            data=df.to_csv(index=False),
            file_name=csv.name,
            mime="text/csv"
        )
