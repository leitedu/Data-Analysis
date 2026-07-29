# ⚡ Energy Market Analytics & Data Engineering Portfolio

Welcome to my central repository for **Energy Market Analytics & Data Engineering projects**. 

This portfolio hosts production-ready Python pipelines, time-series data processing modules, and automated web scrapers, tailored for the **Brazilian Energy Sector** (Electricity & Gas Markets). The projects focus on handling large-scale open data from regulatory and system operator portals like **ONS**, and market agent materials.

## 🧰 Tech Stack & Skills Highlight

* **Languages & Core**: Python (3.10+), Pandas, NumPy.
* **Web Scraping & Automation**: Playwright (Headless Firefox/Chromium), Subprocess execution.
* **Data Engineering Techniques**: Time-series pivoting, deduplication (`groupby`), local file caching, resilient network failure handling (timeouts/SSL).
* **Domain Knowledge**: ONS Open Data standards, ANEEL CEG identification (SIGA), Power Plant dispatch & generation dynamics, Market Nominations & Programmed vs. Executed balancing.

## 📁 Repository Structure

```text
.
├── 📂 ONS Hourly Power Generation/    # Project 1: ONS Hourly Generation Pipeline
│   ├── main.py                         # Execution orchestrator
│   ├── power_generation.py             # Core ETL logic & Playwright scraper
│   ├── requirements.txt                # Project dependencies
│   └── README.md                       # Detailed documentation
│
├── 📂 Natural Gas Nominations/        # Project 2: Nominations & Dispatch Analytics
│   ├── process_nominations.py          # Main script containing ETL logic & chart rendering
│   ├── outputs/
│   │   └── daily_chart.png             # Generated output stackplot chart
│   └── README.md                       # Project documentation
│
├── LICENSE                             # MIT License
└── README.md                           # Main portfolio overview (You are here)
```

## 🚀 Projects Overview
### 1️⃣ ONS Hourly Power Generation Pipeline (`/ONS Hourly Power Generation`)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

**Goal:** Automate the extraction, deduplication, and restructuring of heavy hourly power generation datasets from the Brazilian National Electric System Operator (ONS) to seamlessly extract time-series generation data for a selected set of target power plants.

* **The Problem:** ONS provides massive historical generation CSV files containing millions of records. Manually downloading, filtering, and structuring this volume of data for specific power plants is an inefficient, slow, and resource-intensive process prone to memory bottlenecks.
* **The Solution:** Built an automated, resilient Playwright-powered pipeline with local file caching (`./ons_historical_data`). It efficiently extracts data for user-defined power plants using ANEEL's **CEG** codes, deduplicates timestamp anomalies, and pivots the dataset into an analysis-ready time-series matrix in seconds.

👉 [Explore the ONS Generation Pipeline Documentation & Code](https://github.com/leitedu/Data-Analysis/tree/main/ONS%20Hourly%20Power%20Generation)

### 2️⃣ Natural Gas Dispatch Analytics (`/Natural Gas Nominations`)
![Execution](https://img.shields.io/badge/Execution-Showcase_Only-blue?style=for-the-badge)

**Goal:** Create a structured dataset of daily natural gas nominations and physical dispatches to enable spot market analysis and track short-term delivery imbalances with visual trend insights.

* **The Problem:** Nomination datasets often arrive in fragmented schedules (daily cycles) with non-standardized agent formats, making real delivery flows assessment manual and error-prone.
* **The Solution:** Developed a data transformation and analysis module that ingests daily nomination cycles, constructs and updates a clean time-series database, and generates visual balance charts. This allows quick tracking of delivery variances and spot market fluctuations across the latest nomination days.

👉 [Explore the Nominations Analytics Documentation & Code](https://github.com/leitedu/Data-Analysis/tree/main/Natural%20gas%20nominations)
