

# U.S. - Canada Tariff Impact on Construction and Production sectors (Important note --- update this code for new BCPI added)

## Overview
This Streamlit application is designed to explore the impact of U.S.-Canada tariffs on Canada's production and construction sectors. It provides an interactive interface to visualize key economic indices, specifically the Industrial Product Price Index (IPPI), Raw Materials Price Index (RMPI), and their effects on the Building Construction Price Index (BCPI),specifically residential and non residential buildings within the metal fabrications division. The data was sourced from Statistics Canada. The dashboard allows users to filter data to highlight significant tariff dispute phases (January 2025 implementation and March 2025 lobbying period). Data is scraped and saved as CSV files, accessible via the Data tab.

## Features
- **Interactive Visualization**: Filter IPPI, RMPI, and BCPI data by date to analyze trends from 2020 to June 2025 (latest available data as of the app's creation).
- **Tariff Impact Analysis**: Highlight key tariff phases with customizable date ranges.
- **Data Management**: View and download scraped CSV data in the Data tab.


## How the Code Works
The application is built using Python with the following components:
- **Streamlit**: Provides the web interface for interactivity.
- **Requests and Pandas**: Used to scrape and process Statistics Canada data.
- **Data Fetching**: The `IndexTracker` class in `statcan_scraper.py` fetches data from Statistics Canada using specific Product IDs (PIDs) and filters it based on VECTOR codes (e.g., `v12300998193`).
- **Visualization**: Data is displayed in Trend tabs, with filtering options for start and end dates.



###  Installation
```bash
pip install -r requirements.txt
```

###  Run the App
```bash
streamlit run app.py
```

##  Contributions
Follow the guide in `CONTRIBUTING.md`


## Data Sources
- [Statistics Canada IPPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026501)
- [Statistics Canada RMPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026801)
- [Statistics Canada RMPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810028901)

