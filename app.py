import streamlit as st
import pandas as pd
import os
from src.data_loader import load_data
from src.preprocess import apply_auto_binning
from src.catdap_core import calculate_catdap_aic

st.set_page_config(page_title="CatDAP AIC Evaluator", layout="wide")
st.title("CatDAP AIC Evaluator")
st.markdown("Evaluate single-variable usefulness for binary classification tasks based on AIC.")

# --- Sidebar ---
st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload CSV/XLSX (Optional)", type=["csv", "xlsx"])

DEFAULT_DATA_PATH = "data/10K_Lending_Club_Loans.csv"

with st.spinner("Loading Data..."):
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        df = load_data(DEFAULT_DATA_PATH)

if df.empty:
    st.error("No valid dataset loaded in memory. Please upload a structured CSV or XLSX.")
else:
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    st.sidebar.subheader("Variable Selection")
    
    # Identify initial options
    columns = list(df.columns)
    default_target = "is_bad" if "is_bad" in columns else columns[0]
    
    target_var = st.sidebar.selectbox("🎯 Target Variable (Binary)", columns, index=columns.index(default_target))
    
    available_features = [c for c in columns if c != target_var]
    
    # For MVP assume top 10 as default if many
    default_features = available_features[:10] if len(available_features) > 10 else available_features
    expl_vars = st.sidebar.multiselect("📊 Explanatory Variables", available_features, default=default_features)

    # Binning toggle (always enabled)
    auto_bin = True

    # Validate Binary Target
    unique_target_vals = df[target_var].dropna().nunique()
    if unique_target_vals != 2:
        st.error(f"Target variable `{target_var}` must be binary (found {unique_target_vals} states).")
    elif not expl_vars:
        st.warning("Please select at least one explanatory variable.")
    else:
        if st.sidebar.button("Calculate AIC Rankings", type="primary"):
            with st.spinner("Calculating AIC Distributions..."):
                processed_df = df.copy()
                
                # Automatically exclude high-cardinality categorical variables
                MAX_CAT_LIMIT = 500
                excluded_vars = []
                valid_expl_vars = []
                
                for var in expl_vars:
                    if not pd.api.types.is_numeric_dtype(processed_df[var]) and processed_df[var].nunique() > MAX_CAT_LIMIT:
                        excluded_vars.append(var)
                    else:
                        valid_expl_vars.append(var)
                        
                if excluded_vars:
                    st.warning(f"⚠️ **Skipped Features (High Cardinality):** The following non-numeric variables were excluded because they contain more than {MAX_CAT_LIMIT} unique categories, which is generally unsuitable for group aggregations (like an ID column): \n `{', '.join(excluded_vars)}`")
                    
                if not valid_expl_vars:
                    st.error("No valid features remaining after cleaning. Please select standard categorical or numeric data.")
                    st.stop()
                
                if auto_bin:
                    processed_df = apply_auto_binning(processed_df, valid_expl_vars)
                    
                aic_results = calculate_catdap_aic(processed_df, target_var, valid_expl_vars)
                aic_results['AIC_Diff'] = aic_results['AIC_Diff'].round(2)
                aic_results['Rank'] = range(1, len(aic_results) + 1)
                aic_results = aic_results[['Rank', 'Feature', 'AIC_Diff']]
                
                if aic_results.empty:
                    st.error("No valid calculations emerged. Possibly no variance in features.")
                else:
                    tab1, tab2, tab3 = st.tabs(["🏆 Overall Ranking", "🧊 Cross-Tabulations & Charts", "📚 Appendix"])
                    
                    # Tab 1
                    with tab1:
                        st.subheader("Global Explanatory Power (AIC Difference)")
                        st.markdown("**Lower** (more negative) AIC differences suggest statistically stronger interactions with the target.")
                        
                        st.dataframe(aic_results.set_index('Rank'))
                        csv_ranking = aic_results.to_csv(index=False).encode('utf-8')
                        st.download_button("Download Rankings CSV", data=csv_ranking, file_name="aic_rankings.csv", mime="text/csv")
                        
                    # Tab 2
                    with tab2:
                        # Only show up to 50 individual features to prevent lag, as dictated by Constitution
                        DISPLAY_LIMIT = min(50, len(aic_results))
                        
                        if len(aic_results) > 50:
                            st.warning(f"Display capped to Top {DISPLAY_LIMIT} features for browser UI performance.")
                            
                        top_features = aic_results['Feature'].head(DISPLAY_LIMIT).tolist()
                        
                        import io
                        import zipfile
                        
                        download_placeholder = st.empty()
                        zip_buffer = io.BytesIO()
                        
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                            for feature in top_features:
                                aic_val = aic_results.loc[aic_results['Feature'] == feature, 'AIC_Diff'].values[0]
                                rank_val = aic_results.loc[aic_results['Feature'] == feature, 'Rank'].values[0]
                                st.markdown(f"### Rank {rank_val} - Feature: `{feature}` (AIC: {aic_val})")
                                
                                # Clean up NA matrices for display specifically
                                display_df = processed_df[[target_var, feature]].dropna()
                                cross_tab = pd.crosstab(index=display_df[feature], columns=display_df[target_var])
                                
                                classes = sorted(cross_tab.columns.tolist())
                                if len(classes) == 2:
                                    val0, val1 = classes[0], classes[1]
                                    cross_tab['Total (N)'] = cross_tab[val0] + cross_tab[val1]
                                    cross_tab[f'Count ({target_var}={val1})'] = cross_tab[val1]
                                    cross_tab[f'{target_var} Rate (%)'] = (cross_tab[val1] / cross_tab['Total (N)'] * 100).round(2)
                                    
                                    # Include Total row
                                    cross_tab.loc['All'] = cross_tab.sum(numeric_only=True)
                                    # Recalculate rate specifically for the All row to avoid summing the rates
                                    cross_tab.loc['All', f'{target_var} Rate (%)'] = (cross_tab.loc['All', f'Count ({target_var}={val1})'] / cross_tab.loc['All', 'Total (N)'] * 100).round(2)
                                    
                                    # Add Normalized Rate
                                    all_rate = cross_tab.loc['All', f'{target_var} Rate (%)']
                                    cross_tab['Normalized Rate'] = (cross_tab[f'{target_var} Rate (%)'] / all_rate).round(2) if all_rate > 0 else 0
                                    
                                    cross_tab = cross_tab[['Total (N)', f'Count ({target_var}={val1})', f'{target_var} Rate (%)', 'Normalized Rate']]
                                elif len(classes) > 2:
                                    cross_tab.loc['All'] = cross_tab.sum(numeric_only=True)
                                
                                st.dataframe(cross_tab, use_container_width=True)
                                
                                # Export 
                                csv_ct = cross_tab.to_csv().encode('utf-8')
                                zip_file.writestr(f"Rank{rank_val:02d}_{feature}_crosstab.csv", csv_ct)
                                
                                img_bytes = None
                                html_bytes = None
                                
                                if len(classes) == 2:
                                    import altair as alt
                                    alt.data_transformers.disable_max_rows()
                                    plot_data = cross_tab.drop('All').reset_index()
                                    count_col = f'Count ({target_var}={val1})'
                                    
                                    base = alt.Chart(plot_data).encode(x=alt.X(f"{feature}:N", title=feature))
                                    
                                    bar_total = base.mark_bar(opacity=0.3, color='gray').encode(
                                        y=alt.Y('Total (N):Q', title='Count')
                                    )
                                    
                                    bar_count = base.mark_bar(opacity=0.8, color='steelblue').encode(
                                        y=alt.Y(f'{count_col}:Q', title='Count')
                                    )
                                    
                                    line_rate = base.mark_line(color='#d62728', point=alt.OverlayMarkDef(color='#d62728')).encode(
                                        y=alt.Y('Normalized Rate:Q', title='Normalized Rate', axis=alt.Axis(orient='right'))
                                    )
                                    
                                    bars = alt.layer(bar_total, bar_count)
                                    chart = alt.layer(bars, line_rate).resolve_scale(y='independent')
                                    st.altair_chart(chart, use_container_width=True)
                                    
                                    try:
                                        img_bytes = chart.to_image(format='png')
                                        zip_file.writestr(f"Rank{rank_val:02d}_{feature}_chart.png", img_bytes)
                                    except Exception:
                                        html_bytes = chart.to_html().encode('utf-8')
                                        zip_file.writestr(f"Rank{rank_val:02d}_{feature}_chart.html", html_bytes)
                                else:
                                    st.bar_chart(cross_tab.drop('All', errors='ignore'))
                                
                                # Individual Download Buttons
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.download_button(f"Download {feature} Table", data=csv_ct, file_name=f"crosstab_{feature}.csv", mime="text/csv", key=f"dl_csv_{feature}")
                                with col2:
                                    if img_bytes is not None:
                                        st.download_button(f"Download {feature} Chart (PNG)", data=img_bytes, file_name=f"chart_{feature}.png", mime="image/png", key=f"dl_img_{feature}")
                                    elif html_bytes is not None:
                                        st.download_button(f"Download {feature} Chart (Interactive HTML)", data=html_bytes, file_name=f"chart_{feature}.html", mime="text/html", key=f"dl_html_{feature}")
                                
                                st.divider()
                                
                        # Render Master Download Button
                        zip_buffer.seek(0)
                        download_placeholder.download_button(
                            label="📦 Download All Features Data & Charts (ZIP)",
                            data=zip_buffer,
                            file_name="catdap_all_features.zip",
                            mime="application/zip",
                            type="primary"
                        )
                            
                    # Tab 3
                    with tab3:
                        st.header("📚 Appendix: CatDAP AIC Calculation Logic")
                        st.markdown(r"""
**CatDAP (Categorical Data Analysis Program)** evaluates the predictive power of a given individual explanatory variable $X$ against a target variable $Y$ using Akaike's Information Criterion (AIC).

### The Mathematical Approach

The logic compares two distinct probabilistic models to evaluate how much information is gained by knowing $X$:

1. **Independent Model (aic.0)**: Assumes that $X$ and $Y$ have absolutely no relationship. The probability of any row taking a specific combo of $(X, Y)$ is simply $P(X) \times P(Y)$.
2. **Interaction Model (aic.1)**: Assumes that $X$ and $Y$ are correlated. The probability of any row taking a specific $(X,Y)$ is $P(X,Y)$.

The calculation evaluates the cross-tabulation frequency matrix of features:
- $AIC_0 = -2 \times \text{LogLikelihood}(\text{Independent}) + 2 \times (\text{Categories}(Y) + \text{Categories}(X) - 2)$
- $AIC_1 = -2 \times \text{LogLikelihood}(\text{Interaction}) + 2 \times (\text{Categories}(Y) \times \text{Categories}(X) - 1)$

**AIC Difference (`AIC_Diff`)**
$$ \Delta AIC = AIC_1 - AIC_0 $$

If **$\Delta AIC < 0$**, the interaction model is a statistically better fit than the independent model (penalizing for the degree of freedom complexity). The more negative the value, the more predictive the variable is for determining the target class. Continuous variables upload to this app are automatically split into discrete bins via quantiles prior to calculating these tables.
""")
