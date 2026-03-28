# Feature Specification: CatDAP AIC Evaluator

**Feature Branch**: `001-catdap-aic`  
**Created**: 2026-03-28  
**Status**: Draft  
**Input**: User description: "Build an interactive CatDAP AIC evaluation application with preset data, file upload, feature ranking tab, and cross-tabulation graphics tab."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evaluate Default Dataset (Priority: P1)

Users want to immediately see the value of CatDAP AIC using the default Lending Club loan dataset without needing to prepare their own data first.

**Why this priority**: It establishes baseline trust and demonstrates the tool's core functionality immediately upon load, serving as an interactive tutorial.

**Independent Test**: Can be fully tested by launching the app and verifying the default dataset is loaded, parsed, and its AIC rankings are displayed without any user input.

**Acceptance Scenarios**:

1. **Given** the user opens the application, **When** the UI loads, **Then** the preset data (10K_Lending_Club_Loans.csv) is automatically ingested and `is_bad` is set as the target variable.
2. **Given** the default data is loaded, **When** the user clicks "Calculate AIC", **Then** the application displays an ordered feature ranking table in Tab 1.

---

### User Story 2 - Upload Custom Data and Evaluate Features (Priority: P1)

Data Scientists want to upload their own CSV or XLSX datasets and select target/explanatory variables to evaluate feature usefulness for their specific binary classification tasks.

**Why this priority**: Custom data evaluation is the primary practical use case of the application.

**Independent Test**: Can be fully tested by uploading a valid test dataset, selecting a binary target, computing, and verifying the correct cross-tabulations appear.

**Acceptance Scenarios**:

1. **Given** the user is in the sidebar, **When** they upload a valid dataset, **Then** the feature selectors update to reflect the columns of the new data.
2. **Given** a custom dataset, **When** the user selects a binary target and multiple explanatory variables and calculates AIC, **Then** the system outputs the descending usefulness ranking.

---

### User Story 3 - Deep Dive into Feature Cross-Tabulations (Priority: P2)

Analysts want to visually inspect how the distribution of categories within a specific highly-ranked feature correlates with the target variable.

**Why this priority**: While rankings provide high-level direction, analysts must verify the actual categorical distributions before using features in modeling.

**Independent Test**: Can be fully tested by navigating to the second tab and verifying matching graphical outputs to tabular cross-tabulations.

**Acceptance Scenarios**:

1. **Given** the AIC calculation has completed, **When** the user navigates to Tab 2, **Then** they see vertically stacked cross-tabulation tables ordered by AIC.
2. **Given** the cross-tabulation tables are visible, **When** the user looks at a specific feature, **Then** there is an accompanying visual chart (e.g., stacked bar) reflecting the same data.

---

### User Story 4 - Export Results for External Reporting (Priority: P3)

Users want to download the calculated rankings and cross-tabulations to share them in reports or use them in external data pipelines.

**Why this priority**: Analytical insights often need to be exported for broader organization impact, though not strict for core MVP logic.

**Independent Test**: Test by clicking download buttons and verifying the CSV content matches the UI tables.

**Acceptance Scenarios**:

1. **Given** the results are displayed in Tab 1, **When** the user clicks "Download", **Then** they receive a CSV of the overall feature ranking.
2. **Given** individual feature results in Tab 2, **When** the user clicks "Download" on a specific feature, **Then** a CSV of that specific matrix is downloaded.

### Edge Cases

- What happens when an uploaded dataset has no binary target variable? (Should show an error instructing the user to format their target variable).
- How does system handle explanatory variables with 100% missing values or only 1 unique value? (Should automatically skip them or alert the user rather than crashing).
- How does system handle continuous numeric variables? (Should bin them into quartiles/deciles automatically).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a file uploader supporting `.csv` and `.xlsx` formats up to 50MB.
- **FR-002**: System MUST load a pre-configured demo dataset if no custom file is uploaded.
- **FR-003**: System MUST provide a UI to select one target variable and multiple explanatory variables.
- **FR-004**: System MUST automatically categorize continuous numerical variables using quantile binning before AIC calculation.
- **FR-005**: System MUST calculate the difference in AIC representing the informational gain of each explanatory variable against the target.
- **FR-006**: System MUST drop incomplete records (NA) gracefully on a per-variable basis during cross-tabulation.
- **FR-007**: System MUST display a global ranking table of all calculated variables sorted ascending by AIC.
- **FR-008**: System MUST display individual cross-tabulation matrices alongside visual charts, stacked vertically in AIC rank order.
- **FR-009**: System MUST provide one-click CSV download functionalities for all generated tables.

### Key Entities

- **Dataset**: The ingested structured data containing rows (observations) and columns (features).
- **Target Variable**: A discrete status acting as the dependent variable (e.g., `is_bad`).
- **Explanatory Feature**: A variable (categorical, or continuously binned) being evaluated for its predictive usefulness against the Target.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can upload a 10,000-row file, configure variables, and receive AIC rankings in under 5 seconds.
- **SC-002**: 100% of tested valid CSV/XLSX files are correctly parsed without fatal crashes.
- **SC-003**: The calculated AIC values mathematically match the original R script outputs down to the 4th decimal place.
- **SC-004**: Users are able to independently export their findings within 2 clicks of calculation completing.

## Assumptions

- Users understand basic statistical concepts like target and explanatory variables.
- Uploaded files are essentially flat tables (not deeply nested JSON-style CSVs) with row-headers natively parsable by statistical libraries (e.g., Pandas).
- In-memory calculation is sufficient (no database persistency required).
