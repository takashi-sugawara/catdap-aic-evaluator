<!-- 
Sync Impact Report:
- Version change: none → 1.0.0
- List of modified principles:
  - Added: I. Code Quality
  - Added: II. Testing Standards
  - Added: III. User Experience Consistency
  - Added: IV. Performance Requirements
- Added sections: Development Constraints, Quality Gates
- Removed sections: N/A
- Templates requiring updates (✅ updated / ⚠ pending):
  - ⚠ .specify/templates/plan-template.md 
  - ⚠ .specify/templates/spec-template.md 
  - ⚠ .specify/templates/tasks-template.md
- Follow-up TODOs: None.
-->

# CatDAP AIC Evaluator Constitution

## Core Principles

### I. Code Quality
- **Modularity**: The codebase must be highly modular. Separate data ingestion, the CatDAP AIC calculation logic, and Streamlit UI rendering into distinct modules.
- **Linting & Formatting**: Enforce strict code formatting and linting using `Ruff` or `Black`.
- **Typing**: All function signatures must include comprehensive type hinting (`mypy` static typing is encouraged).
- **Resilience**: Implement defensive programming. Gracefully handle single-variance columns or extensive missing values without crashing.

### II. Testing Standards
- **Core Verification**: The AIC calculation method MUST have dedicated unit tests using `pytest` to ensure mathematical parity with the original R implementation.
- **Edge Cases**: Include testing for edge cases covering identical distributions, single-value columns, and NA handling.
- **Data Integrity**: Verify numeric binning (e.g., using deciles/quartiles via Pandas qcut) comprehensively.

### III. User Experience Consistency
- **Localization**: The application is tailored for a global audience; all UI text, labels, warnings, and documentation MUST be written in clear, professional English.
- **Navigation Structure**: 
  - Tab 1 MUST present the aggregate macro view (Overall Feature Ranking). 
  - Tab 2 MUST present vertically stacked micro views (Individual Feature Cross-Tabulations and charts in AIC-ranked order).
- **Feedback**: Provide immediate visual feedback on interactions (e.g., `st.spinner`).
- **Export**: One-click CSV/Excel export functionalities MUST be consistently placed with every major tabular output.

### IV. Performance Requirements
- **Caching**: Aggressively use Streamlit caching (`@st.cache_data`) for data loading to prevent redundant reads.
- **Computation**: Use vectorized Pandas operations (e.g., `pd.crosstab()`, `np.log()`) instead of loops for frequency calculation.
- **UI Scalability**: Employ optimal UI presentation limits or lazy-loading if processed features exceed 50 to avoid browser rendering delays.

## Development Constraints

- **Generation Scoping**: Avoid arbitrary overwrites of operational code without explicit instruction to ensure manual review.
- **Data Privacy**: Ensure uploaded datasets are strictly handled in-memory and not persisted permanently to the filesystem without explicitly configured storage options.

## Quality Gates

- **Linting & Tests**: Feature additions MUST pass the syntax linter and basic unit tests prior to integration.
- **Dependencies**: All new libraries should be strongly justified to keep the package payload minimal and secure.

## Governance

- This Constitution MUST guide the design, structure, and requirements of the project and supersedes general templates.
- Any amendment, such as introducing new analytical features beyond AIC (e.g., Gini impurity or standard ML feature importances), requires an update to this document.

**Version**: 1.0.0 | **Ratified**: 2026-03-28 | **Last Amended**: 2026-03-28
