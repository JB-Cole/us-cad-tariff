# Instructions: Updating Code for Other IPPIs vs RMPIs Visualizations

This guide provides step-by-step instructions to modify the existing `trends.py` file in your Streamlit app to create visualizations for different IPPIs (Industrial Product Price Indices) and RMPIs (Raw Materials Price Indices) from Statistics Canada. Follow these steps to adapt the code for new product indices.

## Prerequisites
- Ensure you have the `trends.py` file and the `scraper/statcan_scraper.py` file with the `IndexTracker` class available.
- Have access to Statistics Canada product IDs (PIDs) and target product codes for the desired IPPIs and RMPIs (e.g., from the StatCan website).

## Steps to Update the Code

### 1. Identify New Product Indices
- Visit the Statistics Canada page 'https://www150.statcan.gc.ca' to find the PIDs and target product codes for the IPPIs and RMPIs you want to visualize.
  - Example: For Fabricated metal products and construction materials [P63], the PID is `1810026501` and the target product is `v1230995999`.
  - Example: For Metal ores, concentrates and scrap [M61], the PID is `1810026801` and the target product is `v1230998193`.
- Record the new PIDs and target product codes for the indices you wish to compare.

### 2. Update the IndexTracker Instances
- Open `trends.py` and locate the section where `IndexTracker` instances are defined (around lines 20-25).
- Replace the existing `ippi` and `rmpi` instances with the new PIDs and target products. For example:
  ```python
  ippi = IndexTracker(
      pid="NEW_IPPI_PID",
      target_product="NEW_IPPI_TARGET"
  )
  rmpi = IndexTracker(
      pid="NEW_RMPI_PID",
      target_product="NEW_RMPI_TARGET"
  )
- Replace NEW_IPPI_PID, NEW_IPPI_TARGET, NEW_RMPI_PID, and NEW_RMPI_TARGET with the appropriate values from Step 1.

### 3. Adjust Fetch Buttons
- Locate the fetch button sections (around lines 30-60).
- Ensure the fetch_data calls use the updated ippi and rmpi instances. The code should already be generic, but verify it looks like this:
  ```python
  with col1:
    if st.button("🔄 Fetch IPPI"):
        try:
            df_ip = ippi.fetch_data(start=start_date, end=end_date)
            if df_ip.empty:
                st.error("No IPPI data fetched. Check date range or target product.")
            else:
                df_ip.to_csv(data_dir/"ippi.csv", index=False)
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
                if (data_dir/"rmpi.csv").exists():
                    written_df = pd.read_csv(data_dir/"rmpi.csv")
                    st.success(f"✅ Fetched & saved data/rmpi.csv with {len(written_df)} rows")
                    st.dataframe(df_rm)
                else:
                    st.error("Failed to save RMPI CSV.")
        except Exception as e:
            st.error(f"Failed to fetch RMPI: {e}"
            )
- No changes are needed here unless you want to rename the buttons or CSV file names (e.g., change ippi.csv to new_ippi.csv).

### 4. Test the Updated Code
- Run the Streamlit app (streamlit run trends.py).
- Select a date range (e.g., 2020-01-01 to 2025-04-30).
- Click "🔄 Fetch IPPI" and "🔄 Fetch RMPI" to retrieve the new data.
- Click "📈 Generate Comparison Graph" to visualize the updated indices.
- Check for errors in the Streamlit output and verify the data matches the expected range and values.

### 5. Save and Document Changes
- Save the updated trends.py file.
- Update the main page (main.py) to reflect the new indices in the description (mention the new IPPI and RMPI categories).
- Consider adding comments in the code to document the new PIDs and target products for future reference.

### IMPORTANT NOTES
- Ensure the IndexTracker class in scraper/statcan_scraper.py can handle the new PIDs and target products. If errors occur, you may need to debug or modify the scraper logic.
- The CSV files (ippi.csv and rmpi.csv) will be overwritten with new data, so back up existing files if needed.
- If you want to visualize multiple IPPI vs RMPI pairs simultaneously, you’ll need to extend the code to handle multiple IndexTracker instances and merge multiple DataFrames (this requires additional coding beyond these instructions).

### Additional 
- Refer to local_files directory for alternative scraper logic using selinium webdriver. This scraper does not work with streamlit cloud but should work fine on your local machine. 