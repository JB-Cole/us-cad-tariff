import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import streamlit as st


@st.cache_data(show_spinner=False)
def grab_table_from_page(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    table = soup.find('table', {'id': 'simpleTable'})
    if not table:
        raise ValueError("Couldn’t find the table with id 'simpleTable'!")

    thead = table.find('thead')
    header_rows = thead.find_all('tr')
    if len(header_rows) < 2:
        raise ValueError("Not enough rows in <thead> to find date columns!")

    header_row = header_rows[1]
    th_elements = header_row.find_all('th')
    raw_headers = [th.get_text(strip=True) for th in th_elements]
    date_headers = [h for h in raw_headers if h and h.split(' ')[0] in [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']]
    headers = ['Product'] + date_headers

    tbody = table.find('tbody')
    rows = []
    for row in tbody.find_all('tr', class_='highlight-row'):
        th = row.find('th')
        if not th:
            continue
        product_name = th.get_text(strip=True)
        tds = row.find_all('td')
        cell_values = [td.get_text(strip=True) for td in tds]
        cells = [product_name] + cell_values
        if len(cells) == len(headers):
            rows.append(cells)

    df = pd.DataFrame(rows, columns=headers)
    return df


# Button to clear the cache
if st.button("🧹 Clear Cached Data"):
    st.cache_data.clear()
    st.success("Cached data has been cleared.")


class IndexTracker:
    def __init__(self, index_name, page_url, target_product):
        self.index_name = index_name
        self.page_url = page_url
        self.target_product = target_product
        self.data = None

    def fetch_data(self):
        raw_data = grab_table_from_page(self.page_url)
        raw_data['Product'] = raw_data['Product'].str.strip()
        target_clean = self.target_product.split('[')[0].strip()
        filtered_data = raw_data[raw_data['Product'].str.contains(target_clean, case=False, na=False)]

        date_cols = [col for col in raw_data.columns if col != 'Product']
        melted_data = filtered_data.melt(id_vars=['Product'], value_vars=date_cols,
                                         var_name='Reference period', value_name='Value')
        melted_data['Value'] = pd.to_numeric(melted_data['Value'], errors='coerce')
        melted_data['Reference period'] = pd.to_datetime(melted_data['Reference period'], format='%B %Y', errors='coerce')
        melted_data.dropna(inplace=True)
        self.data = melted_data[['Reference period', 'Value']]
        return self.data
