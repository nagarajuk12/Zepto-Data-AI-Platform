# Capstone Project
Capstone Project — Certificate Program in Artificial Intelligence and Machine Learning

## Project Overview

This repository contains the complete capstone project, organized into three modules:

1. **Data Pipeline** — `/data_pipeline`
2. **Analytics** — `/analytics`
3. **Support Assistant** — `/support_assistant`

All three modules are maintained in this single repository.

---

## Repository Structure

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
│   └── README.md                  # Data Pipeline documentation
│   └── web_scraping.py            # Web scraper implementation
│
├── analytics/
│   ├── README.md                  #Analytics documentation
│   ├── *.py
│   └── *.ipynb
│
├── support_assistant/             
│   ├── README.md                 # Support Assistant documentation
│   ├── docs/                     # Raw policy .txt files
│   └── chroma_db/                # Persistent ChromaDB vector store
│   └── embeddings.py             # Document loading, chunking, and embedding logic
│   └── prompt.py                 # System and user prompt builders
│   └── schemas.py                # Pydantic response models (SupportResponse)
│   └── api.py                    # Application entrypoint
│    
├── README.md                      # Project documentation
```
---

## Prerequisites
The project requires:
* python 3
* pip
* git
* beautifulsoup4
* pandas
* requests
* numpy
* chromadb
* sentence-transformers
* langchain-groq
* python-dotenv
* pysqlite3
* pydantic
* fastapi
* uvicorn

To check the installed Python version:

```bash
python --version
```
---

## Installation

Clone the repository:

```bash
git clone https://github.com/nagarajuk12/Zepto-Data-AI-Platform.git
cd Zepto-Data-AI-Platform
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Dependency Strategy

This project uses **one consolidated `requirements.txt` file at the repository root**.

The file contains the Python packages required by all three modules.

---

### Technologies Used
* Python
* Pandas
* NumPy
* Scikit-learn
* SQLite
* FastAPI
* LangChain
* LangGraph
* ChromaDB
---

Note: For each module contains README.md file having more information please go through the same!

---
### Author
Nagaraju Kasa