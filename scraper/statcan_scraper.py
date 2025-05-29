import pandas as pd
import requests
from bs4 import BeautifulSoup


def grab_table_from_page(url: str) -> pd.DataFrame:
    """
    Fetches a Statistics Canada table by URL and returns it as a DataFrame.
    """
    # Pull the raw HTML via HTTP
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'simpleTable'})
    if not table:
        raise ValueError("Couldn’t find the table with id 'simpleTable'!")

    # Extract headers (month-year columns)
    thead = table.find('thead')
    if not thead:
        raise ValueError("No <thead> found in the table!")
    header_rows = thead.find_all('tr')
    if header_rows:
        header_row = header_rows[1] if len(header_rows) > 1 else header_rows[0]
        raw_headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
    else:
        raw_headers = [th.get_text(strip=True) for th in thead.find_all('th')]

    # Identify date-like headers by parsing
    import pandas as _pd
    months = [
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ]
    date_headers = []
    for h in raw_headers:
        # Try month Year format first
        dt = _pd.to_datetime(h, format='%B %Y', errors='coerce')
        if _pd.isna(dt):
            # Try generic parse
            dt = _pd.to_datetime(h, errors='coerce')
        if not _pd.isna(dt):
            date_headers.append(h)
    if not date_headers:
        raise ValueError(f"No date-like columns found in headers! Raw headers: {raw_headers}")
    headers = ['Product'] + date_headers

    # Extract table body rows
    tbody = table.find('tbody')
    if not tbody:
        raise ValueError("No <tbody> found in the table!")
    rows = []
    for tr in tbody.find_all('tr', class_='highlight-row'):
        th = tr.find('th')
        if not th:
            continue
        product = th.get_text(strip=True)
        tds = tr.find_all('td')
        values = [td.get_text(strip=True) for td in tds]
        if len(values) != len(date_headers):
            continue
        rows.append([product] + values)

    if not rows:
        raise ValueError("No data rows extracted from the table!")

    df = pd.DataFrame(rows, columns=headers)
    return df


class IndexTracker:
    """
    Tracks and processes one price index from Statistics Canada.
    """
    def __init__(self, index_name: str, page_url: str, target_product: str):
        self.index_name = index_name
        self.page_url = page_url
        self.target_product = target_product
        self.data: pd.DataFrame | None = None

    def fetch_data(self) -> pd.DataFrame:
        raw = grab_table_from_page(self.page_url)
        # Normalize and filter by product
        raw['Product'] = raw['Product'].str.strip()
        key = self.target_product.split('[')[0].strip()
        df_filtered = raw[raw['Product'].str.contains(key, case=False, na=False)]

        # Melt to long form
        date_cols = [c for c in raw.columns if c != 'Product']
        long = df_filtered.melt(
            id_vars=['Product'],
            value_vars=date_cols,
            var_name='Reference period',
            value_name='Value'
        )
        # Convert types
        long['Value'] = pd.to_numeric(long['Value'], errors='coerce')
        long['Reference period'] = pd.to_datetime(long['Reference period'], format='%B %Y', errors='coerce')
        long.dropna(subset=['Reference period', 'Value'], inplace=True)

        self.data = long[['Reference period', 'Value']].reset_index(drop=True)
        return self.data
