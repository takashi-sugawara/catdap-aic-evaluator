# CatDAP AIC Evaluator Data Model

## Application State Models

### Configuration State
- `target_variable`: String representing the chosen binary dependent column.
- `explanatory_variables`: List of Strings representing the features to analyze.
- `auto_bin_continuous`: Boolean on whether to attempt quantile cuts on detected continuous fields.

### Data Objects
- `RawDataset`: In-memory Pandas DataFrame. Must drop fully `NA` sparse rows upon ingestion.
- `CrossTabMatrix`: An aggregation showing counts where `index=target` and `columns=feature_value`.
- `AicResultRecord`:
  - `feature_name`: String
  - `aic_difference`: Float (lower = better, often negative).

## Mathematical Relationships
- `aic_1` = Interaction model using CrossTabMatrix counts.
- `aic_0` = Independent model using marginal distributions.
- `aic_difference` = `aic_1` - `aic_0`
