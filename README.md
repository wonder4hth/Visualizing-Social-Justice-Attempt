# Visualizing Social Justice – Data Pipeline & FSM Visualization

This repository contains experimental work developed during an internship project focused on **social justice data analysis**.  
The project integrates **web scraping**, **finite state machine (FSM) modeling**, and **visualization** to explore patterns and communicate findings.

---

## 📂 Project Structure

### 1. Data Collection – Web Scraping
- Automated collection of structured and semi-structured data from multiple online sources.
- Techniques:
  - `requests` and `BeautifulSoup` for HTML parsing
  - Handling pagination, dynamic content, and anti-scraping measures
  - Exporting data to CSV/JSON for further processing

### 2. Analysis & Visualization – FSM & Plots
- Built finite state machine models to represent state transitions in the dataset.
- Visualized state transitions and related metrics using:
  - `matplotlib` and `networkx` for FSM diagrams
  - `seaborn` and `plotly` for statistical and interactive visualizations

---

## 🎯 Key Outcomes
- Developed a full pipeline from **data acquisition → modeling → visualization**.
- Created visual narratives to support policy discussions and advocacy.
- Experimented with both static and interactive visualization formats.

---

## 🛠 Tech Stack
- **Python**: `requests`, `BeautifulSoup`, `networkx`, `pandas`, `matplotlib`, `seaborn`, `plotly`
- **Data Formats**: CSV, JSON
