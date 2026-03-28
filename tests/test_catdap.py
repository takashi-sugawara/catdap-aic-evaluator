import pytest
import pandas as pd
from src.catdap_core import calculate_catdap_aic

def test_catdap_aic():
    # Construct an exact mock df
    df = pd.DataFrame({
        'target': [1, 1, 0, 0, 1, 0],
        'feature1': ['A', 'A', 'B', 'B', 'A', 'B'],
        'feature_noise': ['1', '1', '1', '1', '1', '1']
    })
    
    # Feature_noise is completely uniform and has no variance.
    # It should be dropped/skipped automatically and not break.
    result = calculate_catdap_aic(df, 'target', ['feature1', 'feature_noise'])
    
    # Assert feature1 calculates properly
    assert not result.empty
    assert 'feature1' in result['Feature'].values
    assert 'feature_noise' not in result['Feature'].values # skipped due to c2 <= 1
    
    # Let's ensure AIC calculation is consistently mathematical (A & target exactly correlate)
    feat1_row = result[result['Feature'] == 'feature1'].iloc[0]
    
    # c1 = 2 (0, 1), c2 = 2 (A, B) -> perfectly split subset
    assert feat1_row['AIC_Diff'] < 0, "Perfectly correlated variables should yield negative AIC difference"
