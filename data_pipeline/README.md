# Capstone Project
Certificate Program in Artificial Intelligence and Machine Learning

# Module 1: Data Pipeline

## Purpose

The data pipeline is responsible for collecting, cleaning, transforming, validating, and storing the required data.

The pipeline produces the processed dataset required by subsequent analysis modules.

---

## Main Design Decisions

* **Programmatic Data Collection:** Scraped web data programmatically using Python, BeautifulSoup, and pandas.
* **Structured Data Ingestion:** Transformed unstructured HTML elements into standardized tabular structures.
* **Pre-Analysis Data Cleaning:** Validated, cleaned, and standardized fields prior to downstream analysis.
* **Feature Transformation:** Parsed availability information into a Boolean `in_stock` column.
* **Fixed Currency Conversion:** Calculated `price_inr` using a project-defined fixed baseline rate of 1 GBP = 105.50 INR (defined as an artificial constant without external API calls or live rates).
* **Output Standardization:** Saved cleaned and processed records to local CSV format.
* **Consistent Path Management:** Dynamically resolved relative project paths to ensure persistent file storage across scripts and notebooks.

---

## Core Focus Areas

* **Web Scraping:** Automated extraction of product and catalog details from target web sources.
* **Data Cleaning:** Transforming raw scraped data, handling missing values, standardizing formats, and exporting analysis-ready datasets.
* **SQLite Database:** Local relational database design, table creation, and structured schema management.
* **SQL Queries:** Executing analytical queries, including filtering (`WHERE`, `BETWEEN`), distinct counts, joins, and limit operations.

---

## Data Pipeline (/data_pipeline) Structure

```text
Zepto-Data-AI-Platform/
│
├── .venv/                         # Virtual environment (Excluded in the Git)
│
├── data_pipeline/                 # Core ETL and database pipeline
│   ├── query_outputs/             # Exported SQL query results (CSV & TXT)
│   │   ├── query_1_select_where.csv
│   │   ├── query_1_select_where.txt
│   │   ├── query_2_orderby.csv
│   │   ├── query_2_orderby.txt
│   │   ├── query_3_limit.csv
│   │   ├── query_3_limit.txt
│   │   ├── query_4_distinct.csv
│   │   ├── query_4_distinct.txt
│   │   ├── query_5_between.csv
│   │   ├── query_5_between.txt
│   │   ├── query_6_join.csv
│   │   └── query_6_join.txt
│   │
│   ├── books.db                   # SQLite database
│   ├── books_dataset.csv          # Raw scraped dataset
│   ├── cleaned_books_dataset.csv  # Cleaned & processed dataset
│   ├── cleaning_data.ipynb        # Data cleaning workflow
│   └── database_operations.ipynb  # Interactive SQL query execution & operations
│   └── README.md                  # Project documentation
│   └── web_scraping.py            # Web scraper implementation
├── README.md                      # Project documentation
└── analytics/                     # Analytics Module
├── support_assistant/             # Support Assistant Module
│
```