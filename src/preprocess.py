import pandas as pd
import numpy as np

def apply_auto_binning(data: pd.DataFrame, explanatory_vars: list, max_bins: int = None, unique_thresh: int = 10) -> pd.DataFrame:
    """
    Looks for numerical variables that have more unique values than unique_thresh.
    Applies quantile-based binning (`pd.qcut`) safely avoiding duplicates dropping.
    """
    processed = data.copy()
    n_samples = len(data)
    
    # "件数のlog10" -> log10(N)
    if max_bins is None:
        if n_samples > 1:
            max_bins = max(2, int(np.log10(n_samples)))
        else:
            max_bins = 2
            
    for var in explanatory_vars:
        if var not in processed.columns:
            continue
            
        if pd.api.types.is_numeric_dtype(processed[var]) and processed[var].nunique() > unique_thresh:
            try:
                # Extract bin intervals via retbins=True
                _, cut_bins = pd.qcut(processed[var], q=max_bins, retbins=True, duplicates='drop')
                
                labels = []
                for i in range(len(cut_bins)-1):
                    lower = f"{cut_bins[i]:.2f}"
                    upper = f"{cut_bins[i+1]:.2f}"
                    labels.append(f"{i+1}: ({lower} ~ {upper}]")
                    
                processed_col = pd.qcut(processed[var], q=max_bins, labels=labels, duplicates='drop')
                processed[var] = processed_col.cat.add_categories('Missing').fillna('Missing').astype(str)
            except Exception:
                pass # Return original variable if binning fails entirely
                
    return processed
