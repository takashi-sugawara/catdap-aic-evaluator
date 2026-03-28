import streamlit as st
import pandas as pd
import os

@st.cache_data(show_spinner=False)
def load_data(file_or_path) -> pd.DataFrame:
    """
    Loads data from a local payload string path or a streamlit UploadedFile.
    Cached natively by Streamlit.
    """
    try:
        # Default fallback string
        if isinstance(file_or_path, str):
            if not os.path.exists(file_or_path):
                st.error(f"Sample data not found: {file_or_path}")
                return pd.DataFrame()
            return pd.read_csv(file_or_path)
            
        # File object
        file_name = file_or_path.name.lower()
        if file_name.endswith('.csv'):
            return pd.read_csv(file_or_path)
        elif file_name.endswith('.xlsx'):
            return pd.read_excel(file_or_path)
        else:
            st.error("Unsupported file format. Please upload .csv or .xlsx")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Failed to parse source: {e}")
        return pd.DataFrame()
