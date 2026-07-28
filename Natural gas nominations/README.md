# 📊 Natural Gas Nominations ETL & Automated Reporting Pipeline

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Execution](https://img.shields.io/badge/Execution-Showcase_Only-blue?style=for-the-badge)

An automated Python pipeline designed to ingest, clean, and consolidate daily unstructured gas nomination spreadsheets. The system cleans non-standard Excel layouts, maintains an incremental historical master database, and generates visual stackplots for automated daily stakeholder reporting.

> 🔒 **Showcase & Confidentiality Notice**: This repository serves as a portfolio showcase for a production ETL pipeline. To protect sensitive midstream market operations and private corporate data, internal file paths have been replaced with placeholders (`data/sample_daily_update.xlsx`, etc.) and raw input files use anonymized/mock figures.

## 📌 Problem & Solution

### The Challenge
In energy trading and market intelligence, daily gas nomination data is delivered via **private and confidential email spreadsheets**. These reports arrive in non-standardized Excel layouts with changing header structures, boilerplate labels (`TOTAL`, `FINAL`, `CON GAS COMBUSTIBLE`), and redundant sub-totals.

Processing this data manually creates critical bottlenecks:
* **Data Isolation**: High-frequency daily dispatches remain locked in isolated email attachments rather than a structured, queryable historical database.
* **Opaque Market Dynamics**: Without automated aggregation, market analysts cannot easily observe rolling weekly trends to monitor daily player behavior, detect operational shifts, or evaluate supply availability at key import entry points.

### The Solution
This automated Python pipeline provides an end-to-end ETL and analytics workflow:
1. **Ingest & Normalize**: Ingests daily confidential attachments, strips non-standard headers, and sanitizes node identifiers automatically.
2. **Historical Consolidation**: Appends daily records into a master Excel database (`nominations_history.xlsx`), applying strict date deduplication (`FECHA`) to ensure time-series integrity.
3. **Rolling 7-Day Market Analytics**: Isolates the latest 7-day window to render high-resolution stacked area charts (`stackplot`), enabling immediate analysis of player nomination strategies and gas flow dynamics.

## 🌐 Market Background & Industry Relevance

### Why Mutún Matters in LatAm Energy
**Mutún** (located on the Bolivia-Brazil border) serves as the primary physical entry point for imported Bolivian natural gas into the Brazilian gas transportation grid (Gasbol / TBG pipeline system). Historically acting as an important supply backbone for industrial hubs in Southern and Southeastern Brazil, daily volume dynamics at this interconnection node are a critical barometer for regional market balance.

```text
       Bolivia (YPFB Supply/Argentine gas in transit) 
                           │
                           ▼
                  ┌──────────────────┐
                  │    MUTÚN NODE    │  <-- Interconnection Point
                  └────────┬─────────┘
                           │
                           ▼
              Brazilian Gas Grid (Gasbol / TBG)
            (Industrial & Power Generation Demand)
```

### Technical & Market Significance
* Supply Availability & Flow Monitoring: Daily nomination volumes at Mutún reflect real-time physical dispatches versus contractual capacity, offering immediate visibility into supply availability from YPFB (Bolivia) and gas in transit from Argentina to Brazil transported through Bolivian pipeline system.
* Player Dynamics & Dispatch Strategy: Tracking 7-day nomination fluctuations allows analysts to monitor strategic moves by market participants, capacity utilization rates, and operational balancing in response to spot prices or seasonal demand shifts.

## 🛠️ Pipeline Architecture & Workflow

```text
  ┌───────────────────────────┐
  │   Daily Nomination File   │
  │   (Received via Email)    │
  └─────────────┬─────────────┘
                │
                ▼
  ┌───────────────────────────┐
  │  update_nominations_db()  │  • Normalizes headers & strips boilerplate
  │  (Data Cleaning & Merge)  │  • Preserves date column ('FECHA') & cleans 'Mutun' nodes
  └─────────────┬─────────────┘  • Appends to historical DB & deduplicates by date
                │
                ▼
  ┌───────────────────────────┐
  │ nominations_history.xlsx  │  • Master dataset (saved incrementally)
  └─────────────┬─────────────┘
                │
                ▼
  ┌───────────────────────────┐
  │ daily_nominations_chart() │  • Filters node contracts
  │  (Analytics & Plotting)   │  • Formats short column aliases for legibility
  └─────────────┬─────────────┘  • Renders & exports high-resolution stackplot chart
                │
                ▼
  ┌───────────────────────────┐
  │   Output Visual Chart     │
  │    (daily_chart.png)      │
  └───────────────────────────┘
```

## 🚀 Key Features
* 🧹 Robust String & Header Sanitization: Uses pattern substitution and string normalization to clean noisy column names across changing report layouts.
* 🔄 Incremental Database Merging: Appends new daily records while applying deduplication logic on key date fields to guarantee data integrity.
* 📈 Automated Volume Visualization: Renders high-resolution stacked area charts (matplotlib) showing daily nomination distributions per delivery point/node.
* 📧 Email-Ready HTML Generation: Exports clean HTML tables with standardized number formatting (1,000.00) ready to be embedded into automated email dispatches.
* ⚙️ Modular Function Architecture: Clean separation between ETL database updates (update_nominations_db) and visual chart rendering (daily_nominations_chart).

## 📁 Repository Structure
```text
.
├── process_nominations.py         # Main script containing ETL logic & chart rendering
├── outputs/
│   └── daily_chart.png            # Generated output stackplot chart
└── README.md                      # Project documentation
```

## 🧰 Tech Stack
* Pandas: Data cleaning, header manipulation, HTML table export, and time-series deduplication.
* Matplotlib: Automated generation of stacked area charts (stackplot).
