import pandas as pd
import requests, io, zipfile


def grab_table_csv(pid: str) -> pd.DataFrame:
    """
    Fetches the full table CSV (zipped) from the StatCan REST endpoint and returns as a DataFrame.
    pid: table ID string, e.g. '1810026501'
    """
    csv_url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"
    response = requests.get(csv_url)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise ValueError(f"Failed to download CSV for PID {pid}: {e}")

    # The endpoint returns a ZIP archive containing the CSV
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Assume first file in the archive is the CSV
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            df = pd.read_csv(f)
    return df

class IndexTracker:
    """
    Tracks and processes one price index from Statistics Canada.
    """
    def __init__(self, index_name: str, pid: str, target_product: str):
        self.index_name = index_name  # e.g. "IPPI"
        self.pid = pid                # e.g. "1810026501"
        self.target_product = target_product
        self.data: pd.DataFrame | None = None

    def fetch_data(self) -> pd.DataFrame:
        # 1) Download full table via CSV
        df = grab_table_csv(self.pid)

        # 2) Filter rows by target_product substring in 'VECTOR'
        key = self.target_product.split('[')[0].strip()
        filtered = df[df['VECTOR'].str.contains(key, case=False, na=False)]

        # 3) Pivot: index by REF_DATE, columns are VECTOR, values are VALUE
        pivot = filtered.pivot(index='REF_DATE', columns='VECTOR', values='VALUE')
        pivot.index = pd.to_datetime(pivot.index)

        # 4) Select the column matching our target_product and rename it
        matches = [c for c in pivot.columns if key.lower() in c.lower()]
        if not matches:
            raise ValueError(f"Target product not found: {self.target_product}")
        series = pivot[matches[0]].rename(self.index_name)

        # 5) Return tidy DataFrame
        result = series.reset_index()
        result.columns = ['Reference period', 'Value']
        self.data = result
        return self.data
