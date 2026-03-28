# CatDAP AIC Evaluator

A lightweight, powerful Streamlit web application that measures the predictive power of individual explanatory variables against a binary target using the **Categorical Data Analysis Program (CatDAP)** logic based on **Akaike's Information Criterion (AIC)**.

## 🚀 Live Demo
*(Will be available at: [Add your Streamlit Cloud Link here])*

## 📖 Overview
When building binary classification models, determining which features actually contain meaningful predictive signals can be challenging. This tool compares two probabilistic models to measure information gain:
1. **Independent Model ($AIC_0$)**: Assumes the feature and target are completely unrelated.
2. **Interaction Model ($AIC_1$)**: Assumes the feature and target are strictly correlated.

The tool calculates the AIC Difference ($\Delta AIC = AIC_1 - AIC_0$). 
**A more negative AIC difference means that a variable holds a statistically stronger predictive power.**

## ✨ Features
- **Auto Data Preprocessing**: Safely handles numeric types by dynamically binning into categories (`log10(N)`) utilizing quantile intervals.
- **Robust Outlier Management**: Automatically detects and drops high-cardinality string columns (>500 unique values) to prevent computational crashing and overfitting.
- **Cross-Tabulation Analysis**: Automatically calculates target rates across dynamically mapped feature intervals. 
- **Interactive Visualizations**: Beautiful, interactive dual-axis charts overlaying positive counts, total volumes, and standardized baseline target rates across various data layers.
- **Bulk Export Options**: Provides a 1-click option to bulk export all charts (PNG/HTML) alongside cleanly documented CSV tables grouped gracefully into a ZIP.

## 🛠️ Local Installation & Usage
To run this application locally, ensure you have Python 3.9+ installed and clone the repository.

```bash
# Clone the repository
git clone https://github.com/YourUsername/catdap-aic-evaluator.git
cd catdap-aic-evaluator

# Install dependencies
pip install -r requirements.txt

# Run the app locally
streamlit run app.py
```

## 📊 Default Dataset
The application comes pre-bundled with a `10K_Lending_Club_Loans.csv` dataset, designed to demonstrate the predictive strength of different loan attributes (e.g., `grade`, `loan_amnt`, `annual_inc`) in relation to predicting early default (`is_bad` = 1).

## 📄 License
MIT License. Feel free to fork and utilize it for your own Exploratory Data Analysis setups!
