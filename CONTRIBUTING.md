# Contributing to this project

## Reusing the Code for Other Construction/Manufacturing Product Indices
To adapt this code for visualizing other construction or manufacturing product indices from Statistics Canada, follow these steps:

## 1. Identify New Product Indices
Visit the Statistics Canada Data Tables page.
Search for relevant indices (e.g., "Construction Materials," "Manufacturing Products").
Note the Product ID (PID) and the corresponding VECTOR code for the desired index. For example:
IPPI PID: 1810026501, VECTOR: v12300998193
RMPI PID: 1810026801, VECTOR: v12300998199

## 2. Update trends.py
Open or create trends.py (or modify where IndexTracker instances are initialized, likely in app.py).
Add new IndexTracker instances with the new PID and VECTOR code. Example:

```python
from statcan_scraper import IndexTracker

# Existing indices
ippi = IndexTracker(pid="1810026501", target_product="v12300998193")
rmpi = IndexTracker(pid="1810026801", target_product="v12300998199")

# New index (e.g., Construction Materials)
construction_index = IndexTracker(pid="181002XXXX", target_product="v9876543210")  # Replace with actual PID and VECTOR
```
To find the correct VECTOR code, fetch the raw data temporarily (as shown below) and inspect the VECTOR column.

## 3. Modify Data Fetching Logic
Update statcan_scraper.py to handle the new index if needed. The existing grab_table_csv function is PID-agnostic, so it should work with new PIDs. Example debug to find VECTOR codes:

```python
def grab_table_csv(pid: str) -> pd.DataFrame:
    # ... (existing code) ...
    df = pd.read_csv(f, dtype=str)
    print(f"Unique VECTOR values for PID {pid}: {df['VECTOR'].unique()}")
    return df
```
Run the app with the new PID, check the console for unique VECTOR values, and update target_product accordingly.

## 4. Update the Streamlit Interface
In app.py, add a new tab or section to display the new index. Example:

```python
tab1, tab2, tab3 = st.tabs(["IPPI", "RMPI", "Construction Index"])
with tab1:
    st.write(ippi.fetch_data(start=start_date, end=end_date))
with tab2:
    st.write(rmpi.fetch_data(start=start_date, end=end_date))
with tab3:
    st.write(construction_index.fetch_data(start=start_date, end=end_date))
```
Customize the visualization (e.g., charts) using Streamlit’s charting functions (st.line_chart, st.bar_chart) based on the fetched data.

## 5. Test and Deploy
Test locally with the new index to ensure data loads correctly.
Update requirements.txt if new dependencies are added.
Push changes to GitHub and redeploy on Streamlit Cloud.


## Contributing
Fork the repository.
Create a feature branch: `git checkout -b feature/new-index`
Commit changes: `git commit -m "Add new construction index`
Push and open a pull request.


