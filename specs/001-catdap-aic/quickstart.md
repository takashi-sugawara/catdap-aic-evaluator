# Quickstart Guide: CatDAP AIC Evaluator

## Running Locally

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy openpyxl
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Interpreting Results

- Features with **lower (more negative) AIC differences** are more statistically predictive of your target variable.
- Check Tab 2 to visually confirm that the distribution of your target isn't heavily skewed by bad bin sizes.
