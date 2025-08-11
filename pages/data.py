import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Data Preview", layout="wide")
st.title("Data Preview")
st.markdown("Below is the data fetched for Residential and Non-Residential BCPI.")

# Helper function to display a table
def display_table(data_key, label, table_name):
    df = st.session_state.get(data_key, pd.DataFrame())
    if df.empty:
        st.warning(f"No data found for {label}.")
    else:
        st.subheader(label)
        st.dataframe(df)
        st.download_button(
            label=f"Download {table_name}.csv",
            data=df.to_csv(index=False),
            file_name=f"{table_name}.csv",
            mime="text/csv"
        )

# Display both datasets
display_table("df_res", "BCPI Data for Residential Buildings", "BCPI_residential")
display_table("df_nonres", "BCPI Data for Non-Residential Buildings", "BCPI_nonresidential")
display_table("df_ip", "IPPI Data", "IPPI_data")
display_table("df_rm", "RMPI Data", "RMPI_data")
