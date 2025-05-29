# 🤝 Contributing to the Construction Tariff Impact Dashboard

Thank you for your interest in contributing! This dashboard analyzes how tariffs affect Canada's construction industry using public datasets. We're excited to welcome new scrapers, visualizations, and ideas.

---

## 📁 Project Structure Overview

```
construction_tariff_app/
├── app.py                      # Main launcher
├── pages/                      # Visualization dashboards
│   └── trends.py              
├── scraper/                   # Web scraping modules
│   └── statcan_scraper.py     
├── data/                      # Optional: CSV output cache
├── README.md
└── CONTRIBUTING.md
```

---

## 🛠️ Add a New Scraper

1. Create a new file under `scraper/`:
   ```python
   # scraper/lumber_scraper.py
   import pandas as pd

   def fetch_lumber_data():
       # return a DataFrame with at least ['Reference period', 'Value']
       return pd.DataFrame(...)
   ```

2. Create a new visualization page under `pages/`:
   ```python
   # pages/lumber_trends.py
   import streamlit as st
   from scraper.lumber_scraper import fetch_lumber_data

   st.title("Lumber Cost Trends")
   df = fetch_lumber_data()
   st.line_chart(df.set_index("Reference period"))
   ```

3. Your page will automatically show up in the sidebar!

---

## ✅ Scraper Requirements
- Must return a `pandas.DataFrame`
- Must include a datetime column (`Reference period`) and a numeric column (`Value`)
- Use error handling to fail gracefully
- Avoid scraping any source that prohibits it

---

## 🧪 Test Before Pushing
- Run your scraper locally and verify it returns a clean DataFrame
- Check that your Streamlit page renders without errors

---

## 📥 Submit a Pull Request

When you're ready:
1. Fork this repo
2. Create a new branch: `git checkout -b new-feature`
3. Push and open a pull request with:
   - Summary of changes
   - Any new dependencies
   - Sample screenshot (optional)

We’ll review it as soon as possible.

---

Thank you for making this project better! 💡
