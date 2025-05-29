# 🏗️ Construction Tariff Impact Dashboard

This interactive dashboard analyzes the impact of recent U.S.-Canada tariff measures on Canada's construction industry. It uses scraped data from public sources like Statistics Canada to visualize trends in material prices and product indices.

---

## 📦 Project Structure

```
construction_tariff_app/
├── app.py                      # Main app launcher
├── pages/
│   └── trends.py              # IPPI vs RMPI trend visualizer
├── scraper/
│   └── statcan_scraper.py     # Scraper logic for Statistics Canada tables
├── data/                      # (Optional) local data cache
├── requirements.txt           # Python dependencies
├── CONTRIBUTING.md            # Contribution instructions
└── README.md                  # Project overview (this file)
```

---

## 🚀 Getting Started

### 🔧 Installation
```bash
pip install -r requirements.txt
```

### ▶️ Run the App
```bash
streamlit run app.py
```

Use the sidebar to navigate between pages.

---

## 📊 Features

- **RMPI and IPPI** time-series visualizations
- **Modular scraper design**: Add your own web scraping logic
- **Interactive ECharts dashboard** powered by `streamlit-echarts`

---

## 🤝 Contributions

We welcome contributions! To add a new scraper or visualization page:
1. Follow the guide in `CONTRIBUTING.md`
2. Create a new Python file under `scraper/`
3. Add your Streamlit dashboard to `pages/`

Submit a PR when ready!

---

## 📚 Data Sources
- [Statistics Canada IPPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026501)
- [Statistics Canada RMPI](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810026801)
- [CHBA Reports](https://www.chba.ca/) – for qualitative insight

---

## 📬 Contact
Project led by **James Cole**. For questions or contributions, feel free to open an issue.
