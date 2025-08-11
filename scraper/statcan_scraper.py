import pandas as pd
import streamlit as st
import requests, zipfile, io
import logging
logging.basicConfig(filename='logs/scraper.log', level=logging.ERROR)

def grab_table_csv(pid: str) -> pd.DataFrame:
    code = pid[:-2]
    zip_url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{code}-eng.zip"
    print(f"Attempting to download from: {zip_url}")

    try:
        resp = requests.get(zip_url, timeout=30)
        resp.raise_for_status()
        print(f"Download successful. Content length: {len(resp.content)} bytes")
    except requests.RequestException as e:
        print(f"Download failed: {e}")
        return pd.DataFrame()

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            csv_name = next((n for n in z.namelist() if n.lower().endswith(".csv")), None)
            if not csv_name:
                print("No CSV file found in ZIP")
                return pd.DataFrame()
            print(f"Extracting CSV: {csv_name}")
            with z.open(csv_name) as f:
                df = pd.read_csv(f, dtype=str)
                print(f"Raw DataFrame shape: {df.shape}")
                print(f"Sample columns: {list(df.columns)}")
                print(f"Sample VECTOR values: {df['VECTOR'].head().tolist()}")
                return df
    except Exception as e:
        logging.error(f"Error processing ZIP for PID {pid}: {e}")
        print(f"Error processing data: {e}")
        return pd.DataFrame()

class IndexTracker:
    def __init__(self, pid: str, target_product: str):
        self.pid = pid
        self.target_product = target_product.strip()
        self.data = None
        print(f"Initialized with PID: {pid}, Target product: {self.target_product}")
   
    def fetch_data(self, start: pd.Timestamp | None = None, end: pd.Timestamp | None = None) -> pd.DataFrame:
        raw = grab_table_csv(self.pid)
        if raw.empty:
            print("Raw data is empty after download")
            return pd.DataFrame()

        print(f"Full dataset columns: {list(raw.columns)}")
        if "VECTOR" not in raw.columns:
            print("VECTOR column not found in data")
            return pd.DataFrame()

        mask = raw["VECTOR"].str.lower().str.contains(self.target_product.lower(), na=False)
        print(f"Target product (lowercase for match): '{self.target_product.lower()}'")
        print(f"Original target product: '{self.target_product}'")
        print(f"Number of matching rows: {mask.sum()}")
        df = raw.loc[mask, ["REF_DATE", "VALUE"]].copy()
        print(f"Filtered DataFrame shape: {df.shape}")

        if df.empty:
            print("No rows matched the target product filter")
            return pd.DataFrame()

        df.columns = ["Reference period", "Value"]
        df["Reference period"] = pd.to_datetime(df["Reference period"], errors="coerce")
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        print(f"After conversion - NaN in Reference period: {df['Reference period'].isna().sum()}")
        print(f"After conversion - NaN in Value: {df['Value'].isna().sum()}")

        # Debug: Print the range of Reference period
        if not df["Reference period"].isna().all():
            print(f"Reference period range: {df['Reference period'].min()} to {df['Reference period'].max()}")
        else:
            print("All Reference period values are NaN")

        print(f"Start date: {start}, End date: {end}")  # Debug: Confirm passed dates

        if start is not None:
            df = df[df["Reference period"] >= start]
            print(f"After start filter ({start}): {len(df)} rows")
        if end is not None:
            df = df[df["Reference period"] <= end]
            print(f"After end filter ({end}): {len(df)} rows")

        df = df.dropna().sort_values("Reference period").reset_index(drop=True)
        print(f"Final DataFrame shape: {df.shape}")
        self.data = df
        return df