import logging

# Set up logging
logging.basicConfig(
    filename='bcpi_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Logger initialized successfully")


import requests, io, zipfile, pandas as pd

def load_statcan_table(pid: str) -> pd.DataFrame:
    code = pid[:-2]
    zip_url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{code}-eng.zip"
    logging.info(f"Downloading StatsCan table from {zip_url}")

    try:
        resp = requests.get(zip_url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Download failed: {e}")
        return pd.DataFrame()

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            csv_name = next((n for n in z.namelist() if n.endswith(".csv")), None)
            if csv_name:
                with z.open(csv_name) as f:
                    return pd.read_csv(f, dtype=str)
    except Exception as e:
        logging.error(f"Error processing ZIP: {e}")

    return pd.DataFrame()

class BCPITracker:
    def __init__(self, pid: str, target_vectors: list[str]):
        self.pid = pid
        self.target_vectors = [v.strip().lower() for v in target_vectors]
        self.data = None
        logging.info(f"Initialized BCPITracker for PID {pid}")

    def fetch_data(self, start_quarter: str | None = None, end_quarter: str | None = None) -> pd.DataFrame:
        # Step 1 — Download full table using same pattern as IndexTracker
        code = self.pid[:-2]
        zip_url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{code}-eng.zip"
        logging.info(f"Downloading StatsCan table from {zip_url}")

        try:
            resp = requests.get(zip_url, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to load table: {e}")
            return pd.DataFrame()

        try:
            with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                csv_name = next((n for n in z.namelist() if n.endswith(".csv")), None)
                if not csv_name:
                    logging.warning("No CSV file found in ZIP")
                    return pd.DataFrame()
                with z.open(csv_name) as f:
                    df = pd.read_csv(f, dtype=str)
        except Exception as e:
            logging.error(f"Error processing ZIP for PID {self.pid}: {e}")
            return pd.DataFrame()

        # Step 2 — Filter by VECTOR codes
        if "VECTOR" not in df.columns:
            logging.warning("VECTOR column not found in data")
            return pd.DataFrame()

        mask = df["VECTOR"].str.lower().isin(self.target_vectors)
        df = df.loc[mask].copy()
        logging.info(f"Rows after vector filter: {len(df)}")
        if df.empty:
            return pd.DataFrame()

        # Step 3 — Keep only REF_DATE and VALUE, clean up
        df = df[["REF_DATE", "VALUE"]]
        df["REF_DATE"] = pd.to_datetime(df["REF_DATE"], errors="coerce")
        df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")

        # Step 4 — Quarterly filter using real datetimes
        if start_quarter:
            start_dt = pd.Period(start_quarter, freq="Q").start_time
            df = df[df["REF_DATE"] >= start_dt]
        if end_quarter:
            end_dt = pd.Period(end_quarter, freq="Q").end_time
            df = df[df["REF_DATE"] <= end_dt]

        # Step 5 — Add quarter label and finalize
        df["Quarter"] = df["REF_DATE"].dt.to_period("Q").astype(str)
        df = df.dropna().sort_values("REF_DATE").reset_index(drop=True)

        logging.info(f"Final DataFrame shape: {df.shape}")
        self.data = df
        return df



# bcpi = BCPITracker(
#     pid="1810028901",
#     target_vectors=["v1617908010", "v1617908154"]
# )
# df = bcpi.fetch_data(start_quarter="2020Q1", end_quarter="2025Q4")
# print(df)

