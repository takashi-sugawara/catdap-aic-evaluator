# Tasks: CatDAP AIC Evaluator

**Input**: Design documents from `/specs/001-catdap-aic/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directories (`src/`, `data/`, `tests/`) per implementation plan
- [x] T002 [P] Copy the provided `10K_Lending_Club_Loans.csv` to `data/` folder
- [x] T003 [P] Create `requirements.txt` specifying `streamlit`, `pandas`, `numpy`, and `openpyxl`
- [x] T004 Copy the original CatDAP calculation logic block into a new module `src/catdap_core.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement `load_data` utility with `@st.cache_data` caching in `src/data_loader.py`
- [x] T006 [P] Refactor numeric variables binning logic (`pd.qcut`) into `src/preprocess.py`
- [x] T007 Refactor the core AIC calculation method in `src/catdap_core.py` to ensure it gracefully drops `NA` matrices and validates inputs
- [x] T008 [P] Initialize base Streamlit layout in `app.py` with `st.set_page_config` and titles

**Checkpoint**: Foundation ready - basic data flow and core math are established. 

---

## Phase 3: User Story 1 - Evaluate Default Dataset (Priority: P1) 🎯 MVP

**Goal**: Users can immediately see the value of CatDAP AIC using the default Lending Club loan dataset.

**Independent Test**: Load the app, verify it boots with default data, click calculate, and observe Tab 1 ranking table.

### Implementation for User Story 1

- [x] T009 [US1] Load default `data/10K_Lending_Club_Loans.csv` upon app initialization in `app.py` (if nothing uploaded)
- [x] T010 [US1] Build sidebar UI selectors for `target_variable` (defaulting to `is_bad` if present) and `explanatory_variables`
- [x] T011 [US1] Add a "Calculate AIC" action button that triggers the functions from `src/catdap_core.py`
- [x] T012 [P] [US1] Construct the UI for "Tab 1: Overall Ranking", displaying the resulting Dataframe sorted by AIC ascending

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Upload Custom Data and Evaluate Features (Priority: P1)

**Goal**: Allow users to upload their own CSV/XLSX custom data for analysis.

**Independent Test**: Upload an arbitrary CSV, select target/explanatory variables, and verify AIC recalculates.

### Implementation for User Story 2

- [x] T013 [US2] Implement a `st.file_uploader` in the sidebar of `app.py` supporting `.csv` and `.xlsx`
- [x] T014 [US2] Wire the file uploader to `src/data_loader.py` so it supersedes the default dataset
- [x] T015 [P] [US2] Make the UI `selectbox` and `multiselect` dynamically update to the columns of the newly uploaded dataset
- [x] T016 [US2] Ensure standard error handling `st.error` triggers if the dataset contains no valid binary targets

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Deep Dive into Feature Cross-Tabulations (Priority: P2)

**Goal**: Output vertically stacked cross-tabulations and charts for individual highly-ranked features.

**Independent Test**: Switch to Tab 2 and observe `pd.crosstab` matrices accompanied by bar charts.

### Implementation for User Story 3

- [x] T017 [US3] Construct the UI loop for "Tab 2: Individual Feature Details" in `app.py` based on sorted AIC ranking
- [x] T018 [P] [US3] Implement `pd.crosstab(index=target, columns=feature)` display logic for each valid feature in the loop
- [x] T019 [US3] Implement `st.bar_chart` visual render for each cross-tab generation

**Checkpoint**: All visualization user stories should now be independently functional

---

## Phase 6: User Story 4 - Export Results for External Reporting (Priority: P3)

**Goal**: Allow output downloads to external CSV files.

**Independent Test**: Click download CSV and verify content structure.

### Implementation for User Story 4

- [x] T020 [P] [US4] Implement `st.download_button` in Tab 1 for the global AIC ranking table Dataframe
- [x] T021 [US4] Implement `st.download_button` in Tab 2 for each individual cross-tabulation table

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T022 [P] Establish `pytest` unit tests for `src/catdap_core.py` inside `tests/test_catdap.py` to ensure math equates exactly to `.R` counterpart
- [x] T023 Code cleanup, `black` / `ruff` formatting per Constitution
- [x] T024 UI polish: Add `st.spinner("Calculating...")` while CatDAP loop runs to satisfy UX consistency

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1) → User Story 2 (P1) → User Story 3 (P2) → User Story 4 (P3).
- **Polish (Final Phase)**: Depends on all user stories being complete.

### Parallel Opportunities

- Shared base UI templates (T008) and math refactoring (T007) can be executed concurrently.
- Tab 1 generation (T012) and File Upload component (T013) can be built by different developers.
- Formatting, refactoring, and Unit tests (T022, T023) can run continuously alongside phase milestones.
