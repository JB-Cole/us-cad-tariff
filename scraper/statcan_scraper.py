import pandas as pd


def grab_table_csv(pid: str) -> pd.DataFrame:
    """
    Fetches the full table CSV from StatCan REST endpoint and returns as a DataFrame.
    pid: table ID string, e.g. '1810026501'
    """
    csv_url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"
    df = pd.read_csv(csv_url)
    return df

class IndexTracker:
    """
    Tracks and processes one price index from Statistics Canada using the CSV endpoint.
    """
    def __init__(self, index_name: str, pid: str, target_product: str):
        self.index_name = index_name
        self.pid = pid
        self.target_product = target_product
        self.data: pd.DataFrame | None = None

    def fetch_data(self) -> pd.DataFrame:
        # Download full table via CSV
        df = grab_table_csv(self.pid)

        # Keep relevant columns: 'REF_DATE', 'GEO', and specific vector
        # The CSV contains 'Vector', 'REF_DATE', 'VALUE'
        # Filter by target_product in 'Vector' column
        filtered = df[df['VECTOR'].str.contains(self.target_product.split('[')[0].strip(), case=False, na=False)]

        # Pivot: rows are REF_DATE, columns are VECTOR
        pivot = filtered.pivot(index='REF_DATE', columns='VECTOR', values='VALUE')
        pivot.index = pd.to_datetime(pivot.index)

        # Select only the column matching our target_product
        col = [c for c in pivot.columns if self.target_product.split('[')[0].strip().lower() in c.lower()]
        if not col:
            raise ValueError(f"Target product not found in CSV vectors: {self.target_product}")
        series = pivot[col[0]].rename(self.index_name)

        # Build DataFrame with 'Reference period' and 'Value'
        result = series.reset_index()
        result.columns = ['Reference period', 'Value']
        self.data = result
        return self.data
