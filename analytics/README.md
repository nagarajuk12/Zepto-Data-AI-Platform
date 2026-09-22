# Module 2 — Analytics Pipeline

## Purpose

The purpose of this module is to perform exploratory data analysis (EDA),
data cleaning, statistical analysis, visualization, and preparation of the
Titanic dataset for machine learning.

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
│   └── Cleaned Titanic dataset used for modeling
│
├── best_titanic_pipeline.joblib
│   └── Saved complete preprocessing and final model pipeline
│
└── README.md
    └── Documentation for the Analytics Pipeline
```
---
## Execution of the Pipeline
```text
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

```
---
**Handling Of Missing Values**

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

* survived
* pclass
* age
* sibsp
* parch
* fare

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

### IQR Outlier Results

| Variable | Q1 | Q3 | IQR | Lower Bound | Upper Bound | Outlier Count |
|---|---:|---:|---:|---:|---:|---:|
| age | 20.125 | 38.0 | 17.875 | -6.6875 | 64.8125 | 11 |
| fare | 7.9104 | 31.0 | 23.0896 | -26.724 | 65.6344 | 116 |

### Fare Skewness Interpretation

For `fare`:

- Mean = **32.10**
- Median = **14.45**
- Mode = **8.05**

fare_mean > fare_median > fare_mode Therefore, the `fare` distribution is **right-skewed**.

### Survival Rate Results

#### By Sex

| Sex | Survival Rate |
|---|---:|
| female |74.04% |
| male |18.89% |

#### By Passenger Class

| Pclass | Survival Rate |
|---|---:|
| 1 |62.62% |
| 2 |47.28% |
| 3 |24.24% |

#### By Sex and Passenger Class

| Sex | Pclass | Survival Rate |
|---|---:|---:|
| female | 1 |  96.74% |
| female | 2 | 92.11% |
| female | 3 | 50.00% |
| male | 1 | 36.89% |
| male | 2 | 15.74% |
| male | 3 | 13.54% |

### Two Strongest Correlations

The two strongest correlations were identified by comparing the absolute
values of all off-diagonal correlation coefficients. The diagonal values
(`1.000000`) were excluded because they represent each variable correlated
with itself.

#### 1. Passenger Class (`pclass`) and Fare (`fare`)

- Correlation coefficient: **-0.548193**
- Absolute correlation: **0.548193**

There is a moderate negative linear correlation between passenger class and
fare. As the numeric value of `pclass` increases, the fare tends to decrease.
Since lower `pclass` values represent higher passenger classes, this is
consistent with passengers in higher classes generally paying higher fares.

#### 2. Passenger Class (`pclass`) and Age (`age`)

- Correlation coefficient: **-0.336512**
- Absolute correlation: **0.336512**

There is a moderate negative linear correlation between passenger class and
age. As the numeric value of `pclass` increases, passenger age tends to
decrease in this dataset. The relationship is weaker than the correlation
between `pclass` and `fare`.

### Correlation Summary

| Feature Pair | Correlation | Absolute Correlation |
|---|---:|---:|
| `pclass` – `fare` | **-0.548193** | **0.548193** |
| `pclass` – `age` | **-0.336512** | **0.336512** |


### Correlation Matrix

The correlation matrix was calculated using exactly the following six
variables:

- `survived`
- `pclass`
- `age`
- `sibsp`
- `parch`
- `fare`

The variables `adult_male` and `alone` were excluded.

| | survived | pclass | age | sibsp | parch | fare |
|---|---:|---:|---:|---:|---:|---:|
| survived | 1.000000 | -0.335549 | -0.069822 | -0.034040 | 0.083151 | 0.255290 |
| pclass | -0.335549 | 1.000000 | -0.336512 | 0.081656 | 0.016824 | -0.548193 |
| age | -0.069822 | -0.336512 | 1.000000 | -0.232543 | -0.171485 | 0.093707 |
| sibsp | -0.034040 | 0.081656 | -0.232543 | 1.000000 | 0.414542 | 0.160887 |
| parch | 0.083151 | 0.016824 | -0.171485 | 0.414542 | 1.000000 | 0.217532 |
| fare | 0.255290 | -0.548193 | 0.093707 | 0.160887 | 0.217532 | 1.000000 |

### Multivariate Chart 1 — Survival by Passenger Class and Sex

**Interpretation:**  
The chart shows differences in survival rates across passenger classes
and sex. The survival pattern varies between males and females and also
changes across passenger classes.

### Multivariate Chart 2 — Age by Survival

**Interpretation:**  
The box plot shows that the median age is very similar for passengers who
survived and those who did not, with both groups having a median age of
approximately 28 years. The middle 50% of ages also overlaps substantially
between the two survival groups, indicating that age alone does not show a
large difference in the central age distribution. Both groups contain older
age outliers, although the non-survivor group has more extreme high-age
observations.

### Multivariate Chart 3 — Age vs Fare by Survival

**Interpretation:**  
The chart shows the relationship between passenger age, fare, and survival.
Most passengers paid lower fares, while a smaller number of passengers paid
much higher fares. The plot also shows that survived passengers are present
across different ages and fares, with many higher-fare passengers belonging to
the survived group.

### Multivariate Chart 4 — Age by Passenger Class and Survival

**Interpretation:**  
The chart shows the age distribution of passengers across the three passenger
classes and their survival status. Passengers in all three classes are mostly
around the 20–40 age range, but the age distribution varies between classes.
The chart also shows differences in the age distribution between passengers
who survived and those who did not, especially in the third class.

### Standardization Sanity Check

| Variable | Before Mean | Before Std | After Mean | After Std |
|---|---:|---:|---:|---:|
| age | 29.315152 | 12.984932 | 2.717486e-16  |  1.000563 |
| fare | 32.096681 | 49.697504 | 1.398706e-16 | 1.000563 |

After standardization, both `age` and `fare` have means approximately equal
to 0 and standard deviations approximately equal to 1.

## Classification Results

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.809 | 0.783 | 0.691 | 0.734 | 0.861 |
| Decision Tree | 0.764 | 0.681 | 0.721 | 0.700 | 0.750 |
| Random Forest | 0.787 | 0.742 | 0.676 | 0.708 | 0.815 |

### Confusion Matrices

#### Logistic Regression

```text
[[97 13]
 [21 47]]
```

#### Decision Tree

```text
[[87 23]
 [19 49]]
```
#### Random Forest

```text
[[94 16]
 [22 46]]
```

## Imbalance Handling Comparison

| Strategy | Precision | Recall | F1 |
|---|---:|---:|---:|
| Baseline | 0.783 | 0.691 | 0.734 |
| class_weight='balanced' | 0.718 | 0.750 | 0.734 |
| SMOTE | 0.735 | 0.735 | 0.735 |

### Imbalance Interpretation

The baseline produced a precision of **X**, recall of **Y**, and F1 score of
**Z**. The `class_weight='balanced'` approach produced ...

SMOTE produced ...

Based on the observed precision, recall, and F1 values, **[strategy]**
provided the most suitable balance for this project's classification
objective because ...

### OOB Score:

0.808

## Regression Results

| Model | MAE | RMSE | R² | Adjusted R² |
|---|---:|---:|---:|---:|
| Multivariate Linear Regression | 21.1385 | 41.74650 | 0.3467 | 0.2906  |

### Heteroscedasticity Interpretation

The residual plot shows a relatively random distribution of residuals around
zero with no strong increase or decrease in spread across the predicted fare
range. Therefore, there is no strong visual evidence of heteroscedasticity.

### Heteroscedasticity Interpretation

The residual plot shows that the spread of residuals increases as predicted
fare increases. This non-constant residual spread indicates evidence of
heteroscedasticity.

## Final Model Recommendation

Based on the evaluation results, the selected classifier achieved an accuracy
of **X**, precision of **X**, recall of **X**, F1 score of **X**, and AUC of
**X**. These metrics provide information about overall classification accuracy,
positive-class identification, balance between precision and recall, and
ranking performance. The selected model is also saved together with its
preprocessing steps as a single end-to-end pipeline. Therefore, this model
was selected for deployment based on its observed performance for the project's
classification objective.

