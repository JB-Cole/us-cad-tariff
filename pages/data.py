import streamlit as st
import pandas as pd
from db_utils import create_db_engine, query_table

# Check authentication status
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.error("Please log in on the home page to access this content.")
    st.markdown("[Go to Home Page](/)")
    st.stop()

# Page Setup
st.set_page_config(page_title="Data Files", layout="wide")
st.title("Data Preview")
st.markdown("Below is the data saved to the database from your previous fetches.")

# Connect to the database
engine = create_db_engine(
    user='postgres',
    password='1234',
    host='localhost',
    database='tariffdb'
)

# Helper function to fetch and display a table
def display_table(table_name, label):
    try:
        df = query_table(engine, f"SELECT * FROM {table_name}")
        if df.empty:
            st.warning(f"No data found in `{table_name}`.")
        else:
            st.subheader(label)
            st.dataframe(df)
            st.download_button(
                label=f"Download {table_name}.csv",
                data=df.to_csv(index=False),
                file_name=f"{table_name}.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error fetching `{table_name}`: {e}")

# Display both datasets
display_table("ippi_data", "IPPI Data")
display_table("rmpi_data", "RMPI Data")
display_table("bcpi_residential", "BCPI Data for Residential Buildings")
display_table("bcpi_nonresidential", "BCPI Data for Non-Residential Buildings")
