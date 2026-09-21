# Module 2 — Analytics Pipeline

## Purpose

The purpose of this module is to perform exploratory data analysis (EDA),
data cleaning, statistical analysis, visualization, and preparation of the
Titanic dataset for machine learning.

The pipeline covers:

- Loading and profiling the Titanic dataset
- Handling missing values using defined thresholds
- Univariate analysis of `age` and `fare`
- Outlier detection using the IQR method
- Bivariate survival-rate analysis
- Correlation analysis
- Multivariate visualizations
- Standardization sanity checks
- Preparation of cleaned data for modeling

---

## Structure

```text
analytics/
│
├── 01_eda.ipynb
│   └── Data loading, profiling, cleaning, EDA,
│       visualizations, correlation analysis,
│       and standardization checks
│
├── 02_modeling.ipynb
│   └── Machine learning modeling and evaluation
│
├── titanic.csv
│   └── Raw Titanic dataset saved after initial loading
│
├── cleaned_titanic.csv
│   └── Cleaned Titanic dataset
│
└── README.md
    └── Documentation for the Analytics Pipeline
```
---
## Execution of the Pipeline
01_eda.ipynb
      |
      |-- Load Titanic dataset
      |-- Save raw dataset as titanic.csv
      |-- Profile dataset
      |-- Measure missing values
      |-- Handle missing values
      |-- Detect IQR outliers
      |-- Perform univariate analysis
      |-- Perform bivariate analysis
      |-- Perform correlation analysis
      |-- Create multivariate visualizations
      |-- Perform standardization sanity check
      |
      v
cleaned_titanic.csv
      |
      v
02_modeling.ipynb
      │
      ├── Task 7  → Stratified train/test split
      │
      ├── Task 8  → Preprocessing Pipeline
      │
      ├── Task 9  → Logistic Regression
      │             Decision Tree
      │             Random Forest
      │
      ├── Task 10 → Classification evaluation
      │             Confusion matrices
      │             ROC/AUC
      │             Comparison table
      │
      ├── Task 11 → Imbalance comparison
      │             Baseline
      │             class_weight='balanced'
      │             SMOTE
      │
      ├── Task 12 → Random Forest GridSearchCV
      │             Best parameters
      │             OOB score
      │
      ├── Task 13 → Multivariate Linear Regression
      │             MAE
      │             RMSE
      │             R²
      │             Adjusted R²
      │             Residual plot
      │
      ├── Task 14 → Final model comparison
      │             Classification metrics
      │             Regression metrics
      │             3–5 sentence recommendation
      │
      └── Task 15 → Save complete pipeline
                    Reload pipeline
                    Predict from raw input

Execution Steps
1. Open 01_eda.ipynb.
2. Load the Titanic dataset using Seaborn.
3. Immediately save the raw dataset as titanic.csv.
4. Profile the dataset and calculate missing-value percentages.
5. Apply the required missing-value handling strategies.
6. Save the cleaned dataset as cleaned_titanic.csv.
7. Perform univariate, bivariate, and multivariate analysis.
8. Perform the correlation analysis using the required six columns.
9. Perform the standardization sanity check for age and fare.
10. Open 02_modeling.ipynb.
11. Load cleaned_titanic.csv.
12. Perform train/test splitting and model preprocessing.
13. Train and evaluate the machine learning models.
    The standardized data created during the EDA sanity check is used only
    for analysis. It is not passed to the modeling pipeline. Modeling performs
    its own preprocessing using the training data only
## Interpretations
**Missing Values**

The missing-value strategy is based on the percentage of missing values in
each column:

Less than 5% missing: affected rows are dropped.
5%–30% missing: values are imputed.
More than 30% missing: the column is either dropped or missing values are
explicitly encoded, with the decision justified.

For the Titanic dataset, age requires imputation because it has a
moderate percentage of missing values. deck has a high percentage of
missing values, so missing values are represented as Unknown rather than
using unreliable numerical imputation.

**Univariate Analysis**

The age and fare distributions are examined using histograms and
box plots.

The IQR method is used to identify potential outliers:

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

For fare, the mean, median, and mode are compared to understand the shape
of the distribution. A distribution where the mean is greater than the
median is consistent with positive/right skewness.

**Bivariate Analysis**
Survival rates are compared across:

Sex
Passenger class
Sex and passenger class together

Boolean masking with & and | is used for the required subgroup
comparisons.

The correlation matrix contains exactly these six numerical variables:

survived
pclass
age
sibsp
parch
fare

The two strongest correlations are identified using the absolute value of
the off-diagonal correlation coefficients. The sign of each original
correlation is retained when interpreting the relationship.

**Multivariate Analysis**

Multiple visualizations are used to examine relationships between several
variables simultaneously, including:

Survival by passenger class and sex
Age distribution by survival
Age versus fare by survival
Age distribution across passenger classes and survival

These visualizations help identify patterns that may not be visible when
examining individual variables separately.

**Standardization**

age and fare are standardized using the z-score transformation:

z = (x - mean) / standard deviation

After standardization, the variables should have approximately:

Standard deviation ≈ 1

This check is performed as part of EDA and is separate from the modeling
preprocessing pipeline.

---
## Results/Interpretation

### Missing-Value Results

| Column | Missing % | Strategy | Threshold Justification |
|---|---:|---|---|
| age | 19.87% | Median imputation | 5%–30% → impute |
| embarked | 0.22% | Drop affected rows | <5% → drop rows |
| embark_town | 0.22% | Drop affected rows | <5% → drop rows |
| deck | 77.22% | Encode as `Unknown` | >30% → encode missing category |

### 2. IQR outlier counts
### IQR Outlier Results

| Variable | Q1 | Q3 | IQR | Lower Bound | Upper Bound | Outlier Count |
|---|---:|---:|---:|---:|---:|---:|
| age | ACTUAL | ACTUAL | ACTUAL | ACTUAL | ACTUAL | ACTUAL |
| fare | ACTUAL | ACTUAL | ACTUAL | ACTUAL | ACTUAL | ACTUAL |