# ⚡ ONS Hourly Power Generation ETL Pipeline

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Fully_Runnable-success?style=for-the-badge)

An automated Python ETL pipeline designed to extract, transform, and consolidate hourly power generation data from the Brazilian National Electric System Operator (ONS) open data portal. 

This script automates the downloading of massive historical datasets, filters the data for specific power plants based on user a input list, deduplicates hourly anomalies, and reshapes the data into a clean, analysis-ready time-series format.


## 📌 Problem & Solution

Analyzing historical power generation in Brazil requires dealing with massive raw CSV files hosted on AWS S3 from the National System Operator (ONS), which often face connection timeouts when accessed via standard HTTP requests. Furthermore, the raw data is formatted in a "long" structure (millions of rows) with occasional duplicate entries for the same timestamp.

**This pipeline solves this by:**
1. **Resilient Extraction**: Uses Playwright (Headless Browser) to simulate human navigation, bypassing AWS firewall and connection timeout constraints (`WinError 10060`).
2. **Smart Caching**: Downloads and stores raw data locally (`./ons_historical_data`). Subsequent runs read directly from the disk, saving bandwidth and execution time.
3. **Data Wrangling**: Uses Pandas to parse timestamps, group/deduplicate hourly records using `.mean()`, and pivot the dataset so each column represents a specific power plant, making it ready for BI tools or statistical modeling.


## 🔍 What is a CEG & How to find it?

To run this pipeline, you need to provide a list of **CEG** codes. 

**What is it?**
CEG stands for *Código Único de Empreendimentos de Geração* (Generation Facility Unique Identification Code) . It is a unique alphanumeric identifier assigned by ANEEL (the Brazilian Electricity Regulatory Agency) to every single power plant in the country (e.g., Hydro, Wind, Solar, Biomass). 
*Example format: `UHE.PH.MG.000000-0.01`*


**How to find a plant's CEG:**
1. Go to the **[SIGA ANEEL Portal]([https://siga.aneel.gov.br/](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel/resource/11ec447d-698d-4ab8-977f-b424d5deee6a))** (Sistema de Informações de Geração da ANEEL - ANEEL's Generation Information System).
2. Use the search filters (by State, Company, or Plant Name).
3. Locate the desired power plant in the table and copy the value from the `CEG` column.


## 📅 Dataset Structure & Timeframe

The ONS Open Data portal provides historical generation records starting from **2001 onwards**. However, the file structure changes depending on the requested year:

* **2001 to 2021 (Annual):** Data is bundled into massive yearly files (e.g., `GERACAO_USINA_2021.csv`).
* **2022 Onwards (Monthly):** Due to the increasing volume of hourly records (driven by the boom in wind and solar plants), recent data is split into monthly files (e.g., `GERACAO_USINA_2022_01.csv`).

*The pipeline's `process_ons_generation()` function automatically identifies the requested timeframe and handles this structural transition seamlessly.*


## ⚠️ Performance & File Size Note

* **Heavy Payloads**: The ONS raw CSV files are heavy (annual files can be hundreds of megabytes, and monthly files average ~50MB each).
* **Execution Time**: The **first execution** covering multiple years will take several minutes to download all files. Please be patient and do not interrupt the terminal.
* **Cached Runs**: Thanks to the built-in caching system, running the script a second time for the same period will take only seconds, as it reads the `.csv` files directly from your local drive.


## 🚀 Quick Start

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install firefox
   
2. Configure your target plants:
Open main.py, define your output file name, and list the CEGs of the desired power plants:
```python
from power_generation import process_ons_generation

# Configuration Variables
OUTPUT_NAME = 'generation_database.xlsx' 
CEGS = [
        'UHE.PH.PR.001161-4.01',  # Plant A Example - Itaipu hydroelectric power plant
        'UTN.UR.RJ.000101-5.01'   # Plant B Example - Angra 2 nuclear power plant
        ] 

if __name__ == "__main__":

    # Extracts data from 2021 to 2023 for the specified plants
    process_ons_generation(cegs=CEGS, start_year=2021, end_year=2023, end_month=12, output_name=OUTPUT_NAME)
```

3. Run the orchestrator:
```bash
   python main.py
```

## 📊 Output Data Structure

The pipeline aggregates the hourly raw data, parses the timestamp, and pivots the selected power plant CEGs into columns. Below is a sample of the generated `generation_database.csv`:

| din_instante | Date | Hour | UHE.PH.PR.001161-4.01 | UTN.UR.RJ.000101-5.01 |
|---|---|---|---|---|
| 2023-01-01 00:00:00 | 2023-01-01 | 00:00:00 | 1772.63 | 1358.50 |
| 2023-01-01 01:00:00 | 2023-01-01 | 01:00:00 | 1734.80 | 1358.90 |
| 2023-01-01 02:00:00 | 2023-01-01 | 02:00:00 | 1780.29 | 1358.70 |
| 2023-01-01 03:00:00 | 2023-01-01 | 03:00:00 | 1766.30 | 1358.70 |

## 🧰 Tech Stack
* **Pandas:** Data manipulation, datetime parsing, deduplication (groupby), and reshaping (pivot).
* **Playwright (sync_api):** Robust headless web scraping and automated file downloading.
* **Pathlib & OS:** Cross-platform local cache directory management.
