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

## Expected Output

The pipeline should generate the required to be processed dataset, for example:

```text
data_pipeline/
└── books_dataset.csv
```

The generated dataset contains the fields required by the project specification, including the parsed `in_stock` Boolean field.

---
## Currency convertion
```text
Currency conversion: price_inr is calculated using the project-defined fixed baseline rate of 1 GBP = 105.50 INR. This is an artificial constant defined for this assignment and does not use a live or historical exchange rate or an external API.
```