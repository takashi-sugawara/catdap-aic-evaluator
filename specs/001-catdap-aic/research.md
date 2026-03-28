# Research Notes: CatDAP AIC Evaluator

## Unknowns Resolved

- None originally in Technical Context. The math functions are standard `pandas` and `numpy`. 
- **Tech Stack Check**: Streamlit is perfectly suited for this quick, locally-hosted data analytical tool compared to heavy frontend frameworks because it has built-in caching (`@st.cache_data`) and effortless dataframe rendering.

## Technology Choices

1. **Caching Engine**
   - **Decision**: Streamlit `@st.cache_data`
   - **Rationale**: Safe for serialization of uploaded datasets and highly native to the stack.
   - **Alternatives**: Manually saving to SQLite (discarded due to privacy constraints in Constitution and being overkill).

2. **Categorical Binning Strategy**
   - **Decision**: `pandas.qcut` internally. 
   - **Rationale**: Replicates original CatDap R implementation assumptions best for continuous variables.
   - **Alternatives**: `pandas.cut` (discarded as it may result in entirely empty bins which breaks the logarithmic calculation of cross-tabs).
