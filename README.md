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
capstone-project/
│
├── README.md
├── requirements.txt
│
├── data_pipeline/
│   ├── README.md
│   ├── *.py
│   └── *.ipynb
│
├── analytics/
│   ├── README.md
│   ├── *.py
│   └── *.ipynb
│
└── support_assistant/
    ├── README.md
    ├── *.py
    └── *.ipynb
```

---

## Prerequisites

The project requires:

* Python 3.14.6
* pip
* Git
* beautifulsoup4 4.15.0
* pandas 3.0.5
* requests 2.34.2
* numpy 2.5.3

Check the installed Python version:

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

# Module 1: Data Pipeline

## Purpose

The data pipeline is responsible for collecting, cleaning, transforming, validating, and storing the required data.

The pipeline produces the processed dataset required by the subsequent analysis.

## Main Design Decisions

* Data is collected programmatically.
* Raw data is converted into a structured format.
* Data is cleaned before analysis.
* Availability information is converted into a Boolean `in_stock` column.
* Processed data is saved as a CSV file.
* File paths are handled so that generated data is stored consistently within the project.

## How to Run

From the repository root:

```bash
python data_pipeline/web_scraping.py
```

Replace `web_scraping.py` with the actual entry-point file.

## Expected Output

The pipeline should generate the required to be processed dataset, for example:

```text
data_pipeline/
└── books_dataset.csv
```

The generated dataset contains the fields required by the project specification, including the parsed `in_stock` Boolean field.

---

