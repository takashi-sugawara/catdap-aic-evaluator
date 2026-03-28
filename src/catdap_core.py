import pandas as pd
import numpy as np
from typing import List

def calculate_catdap_aic(data: pd.DataFrame, target: str, var_list: List[str]) -> pd.DataFrame:
    """
    Calculate CatDAP AIC for a given set of explanatory variables against a target variable.
    
    Returns a DataFrame ranked by AIC_Diff ascending (lower is better, theoretically negative).
    """
    results = []
    
    # defensive programming check
    if data.empty or target not in data.columns:
        return pd.DataFrame()
        
    for var in var_list:
        if var not in data.columns:
            continue
            
        # extract data and drop NAs specifically for interaction
        df_subset = data[[target, var]].copy().dropna()
        n_subset = len(df_subset)
        if n_subset == 0:
            continue
            
        c1 = df_subset[target].nunique()
        c2 = df_subset[var].nunique()
        
        # If there's no variation, calculation becomes degenerate
        if c1 <= 1 or c2 <= 1:
            continue
            
        # Interaction Model (aic.1)
        df_freq = df_subset.groupby([target, var]).size().reset_index(name='Freq')
        df_freq = df_freq[df_freq['Freq'] > 0]
        
        freq_log_freq_1 = (df_freq['Freq'] * np.log(df_freq['Freq'])).sum()
        aic_1 = (-2) * (freq_log_freq_1 - n_subset * np.log(n_subset)) + 2 * (c1 * c2 - 1)
        
        # Independent Model (aic.0)
        target_freq = df_subset[target].value_counts()
        var_freq = df_subset[var].value_counts()
        
        sum_freq_log_freq = (target_freq * np.log(target_freq)).sum() + (var_freq * np.log(var_freq)).sum()
        aic_0 = (-2) * (sum_freq_log_freq - 2 * n_subset * np.log(n_subset)) + 2 * (c1 + c2 - 2)
        
        aic_diff = aic_1 - aic_0
        results.append({
            'Feature': var,
            'AIC_Diff': aic_diff
        })
        
    if not results:
        return pd.DataFrame()
        
    aic_rank = pd.DataFrame(results)
    return aic_rank.sort_values('AIC_Diff').reset_index(drop=True)
