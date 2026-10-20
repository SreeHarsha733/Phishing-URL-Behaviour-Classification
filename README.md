\# Phishing URL Behaviour Classification



\## Overview

A binary machine learning classifier that detects phishing (malicious) URLs based on structural and lexical characteristics of the raw URL string, with a Streamlit demo app for real-time predictions. Built as a capstone project for Learn Depth Academy LLP (Track 1, Problem 02).



\## Problem Statement

Phishing URLs attempt to mimic legitimate websites to steal credentials or sensitive data. This project builds a supervised ML model that classifies a given URL as \*\*benign\*\* or \*\*malicious\*\* using only features derivable from the URL string itself — no external API calls, WHOIS lookups, or page content required.



\## Dataset

\- \*\*Source:\*\* Combined dataset of 450,176 URLs — malicious URLs from PhishTank, benign URLs from Majestic Million.

\- \*\*Columns:\*\* `url` (raw URL string), `label` (benign/malicious), `result` (0/1 target).

\- \*\*Class distribution:\*\* 76.8% benign, 23.2% malicious (imbalanced — handled via stratified train/test split and precision/recall/F1 reporting rather than accuracy alone).

\- \*\*Data quality:\*\* No missing values, no duplicate rows.



\## Feature Engineering

Since the raw dataset contains only the URL string, 21 structural and lexical features were engineered per URL, including:

\- Length features: `url\_length`, `hostname\_length`, `path\_length`, `query\_length`

\- Character-level: `digit\_count`, `digit\_ratio`, `special\_char\_count`, `dot\_count`, `slash\_count`, `hyphen\_count`, and counts of `@ ? \& = % \_`

\- Domain features: `subdomain\_count`, `has\_https`, `has\_ip`, `has\_www`

\- Content signal: `suspicious\_keyword` (presence of terms like "login", "verify", "secure", "bank")



\## Models

Two baseline models were trained and compared:



| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |

|---|---|---|---|---|---|

| Logistic Regression | 99.67% | 99.28% | 99.29% | 99.28% | 99.79% |

| Decision Tree | 99.71% | 99.62% | 99.12% | 99.37% | 99.77% |



\*\*Final model: Logistic Regression\*\* — selected for its marginally higher ROC-AUC, smoother/better-calibrated probability outputs (relevant for the app's risk-score display), and more interpretable coefficients for explaining feature influence.



\### Note on feature importance

`has\_https` is the strongest predictive feature in this dataset — nearly all benign (Majestic Million) URLs use HTTPS, while a large share of malicious (PhishTank) URLs do not. This reflects a characteristic of how the two source datasets were collected, not a universal rule that HTTPS implies safety. The model should be understood as reflecting this dataset's patterns rather than a general phishing law.



\## Project Structure

phishing url

│

├── urldata.csv

├── model.ipynb

├── phishing\_model.pkl

├── scaler.pkl

├── app.py

├── requirements.txt

└── README.md



\## How to Run

1\. Install dependencies:pip install -r requirements.txt

2\. (Optional) Re-run the notebook `phishing\_url\_model.ipynb` to regenerate the model from scratch.

3\. Launch the Streamlit app:streamlit run app.py

4\. Enter a URL in the input box and click \*\*Analyze\*\* to see the prediction and risk probability.



\## Limitations

\- Model performance is dataset-specific; results may not generalize to phishing techniques not represented in PhishTank at the time of collection (e.g., HTTPS-enabled phishing sites).

\- No deep learning or content/HTML-based analysis was used, per project scope — only URL-string-derived features.

\- Real-world deployment would benefit from periodic retraining as phishing patterns evolve.



\## Author

Bolla Sree Harsha — Learn Depth Academy LLP  Machine Learning Intern

