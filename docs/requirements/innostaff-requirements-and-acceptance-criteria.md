# InnoStaff Workforce Solutions Requirements and Acceptance Criteria

**Version:** 0.1  
**Status:** Draft for review  
**Project:** InnoStaff  
**Suggested repository location:** `docs/requirements/innostaff-requirements-and-acceptance-criteria.md`

## 1 Purpose

This document defines what InnoStaff must deliver and the evidence required to demonstrate completion. It translates the approved project handoff into verifiable requirements. Detailed columns, formulas, benchmark procedures, and screen layouts belong in their respective design documents and must remain consistent with this scope.

InnoStaff is a software engineering portfolio project centered on advanced SQL Server database engineering. It combines a normalized relational database, reproducible synthetic workforce data, seven SQL investigations, three measured query optimization case studies, and a lightweight Streamlit dashboard. Its primary audience is recruiters and technical interviewers evaluating SQL design, correctness, performance engineering, and business reasoning.

## 2 Business context and objectives

InnoStaff Workforce Solutions is a fictional staffing agency serving the greater San Francisco Bay Area, including San Francisco, San Jose, Santa Clara, Palo Alto, Oakland, Alameda, and Fremont. It supplies fictional technology companies with contract workers.

The primary business problem is early turnover in high-volume entry-level technical operations placements, including autonomous vehicle operators, robot operators, teleoperators, vehicle test operators, and similar roles. Advertised compensation and applicant interest do not necessarily translate into sustained placement retention. Repeated replacement hiring creates additional recruiting and onboarding demand.

Intermediate operations roles and experienced software, networking, systems, IT, and cybersecurity positions provide context and comparison. They must not displace the primary investigation of accessible entry-level operations roles.

The project must answer two questions:

1. Which observed factors and combinations are associated with early placement exits and sustained retention within the synthetic dataset?
2. Which operational improvements do those findings support, and what could their business impact be under explicit hypothetical assumptions?

Success means defensible analysis and reproducible engineering evidence. No predetermined retention improvement, statistical finding, or performance speedup is required.

## 3 Scope boundaries

### Included

- Microsoft SQL Server schema, constraints, historical records, reporting objects, and indexes.
- Fixed-seed Python data generation, a full demonstration dataset, and a small deterministic CI dataset.
- Seven SQL investigations defined in Section 6.
- Three documented optimization case studies with real measurements and result validation.
- Five SQL-backed Streamlit pages under the name **InnoStaff Workforce Intelligence**.
- Automated correctness checks, GitHub Actions CI, Docker Compose local setup, and project documentation.

### Excluded

- Authentication, account administration, and unrelated CRUD workflows.
- A full React frontend, microservices, machine learning, and AI features.
- Unnecessary Azure infrastructure or technology added solely to enlarge the stack.
- Real worker records, real client records, proprietary employer information, and claims of affiliation with real employers.
- Causal claims about turnover based solely on descriptive synthetic associations.
- Payroll or tax modeling unless scope is explicitly revised. Gross wages less commuting expenses must not be labeled net take-home pay.

A read-only hosted Streamlit demo backed by Azure SQL Database is optional. Local reproducibility and the complete local dataset are required; paid hosting is not a completion gate.

## 4 Database and synthetic data requirements

### DB-01 Relational model

Implement a normalized SQL Server model supporting workers, career goals, clients, client sites, recruiting branches, recruiters, job roles, job orders, hiring cohorts, placements, shift assignments, commute assessments, training records, worker surveys, attendance, career events, and exit records.

**Acceptance criteria**

- An ERD and data dictionary identify tables, columns, data types, nullability, keys, relationships, constraints, and important design decisions.
- The 17 conceptual entities in the handoff are represented. Any justified refinement is documented in the database design; table count alone is not a quality target.
- A worker can have multiple placements. A placement ending is distinguishable from the worker leaving the agency.
- Dated assessments, schedules, goals, and career events preserve history needed for time-aware analysis rather than overwriting relevant prior states.

### DB-02 Integrity and valid timelines

Enforce structural integrity in SQL Server and validate business rules through constraints or explicit checks appropriate to their complexity.

**Acceptance criteria**

- Primary keys, foreign keys, appropriate unique constraints, check constraints, and nullability are implemented.
- Tests detect invalid pay, unsupported statuses, reversed date ranges, orphaned references, inconsistent exits, impossible attendance dates, and career events outside valid employment timelines.
- Representative invalid inserts or updates are rejected or flagged by documented validation. Cross-table rules need not be forced into unsupported check constraints.
- Transactions protect multi-step changes where partial completion would leave inconsistent data.

### DATA-01 Dataset scale and reproducibility

The initial full dataset targets are **25,000 workers, 60,000 placements, approximately 750,000 attendance records, approximately 150 clients, and 36 months of activity**. These are design targets rather than immutable limits; deviations require a documented rationale.

**Acceptance criteria**

- A documented fixed seed and configuration regenerate the same logical records under the documented generator version and environment.
- The generator supports both the full dataset and a small CI dataset without manual record editing.
- Generated foreign keys and timelines are valid, and the full dataset loads successfully.
- The methodology states the coverage and grain of attendance records; the target count must not silently imply a complete daily attendance census for every placement.
- The generator represents varied regions, roles, compensation, commutes, schedules, training experiences, career aspirations, and outcomes.
- Positive, neutral, and negative experiences coexist. Interactions and confounders are represented without making every hypothesis true by construction.
- Synthetic mechanisms, assumptions, and limitations are disclosed. All companies, people, and business records are fictional; public geographic names may provide regional context.

## 5 Analytical correctness requirements

### AN-01 Retention definitions and observation windows

Measure placement retention at 30, 60, and 90 days using a documented analysis cutoff and consistent eligibility rules.

**Acceptance criteria**

- Each threshold uses placements with sufficient observation time under the documented metric definition. Incomplete windows are identified separately rather than treated as successful retention or early exits.
- Outputs expose eligible counts and retained counts alongside rates; denominators are inspectable.
- The investigation plan defines day-boundary handling, start and end date semantics, active placements, exit classifications, and which terminations count toward each metric before query implementation.
- Known-answer fixtures cover an early exit, active placement with sufficient follow-up, incomplete observation window, exit at a threshold boundary, and a worker with multiple placements.
- Cohort comparisons use consistent definitions and show sample sizes. Sparse segments and unavailable comparisons are identified.

### AN-02 Time-aware comparisons and interpretation

**Acceptance criteria**

- Assessments and events are matched to their relevant placement and date; repeated survey or attendance rows do not accidentally multiply placement counts.
- A survey recorded after an exit or a promotion after the first 90 days is not treated as a pre-existing explanation of that placement's first-90-day outcome.
- Career mobility analysis uses documented time-based comparisons that address survivorship and immortal-time bias.
- Combined-pattern analysis compares relevant strata or comparable groups and explains remaining confounding and missing data.
- Findings describe associations within generated data. Worker-reported perceptions remain identifiable as subjective assessments.
- Wages, commute costs, and estimated savings display units, time basis, formulas, and assumptions. Hypothetical estimates are distinguished from calculated synthetic outcomes.

## 6 Seven required SQL investigations

Each investigation must have its own executable script, documented metric definitions, interpretable outputs, and correctness checks. The investigation plan will specify detailed query design without adding investigations.

### INV-01 Retention baseline and hiring cohorts

**Script:** `analysis/01_retention_baseline.sql`

**Acceptance:** Reports placement counts, 30/60/90-day retention, differences by role, client, site, and hiring cohort, time trends, and replacement versus growth hiring. Applies AN-01 and shows eligible denominators.

### INV-02 Commute economics

**Script:** `analysis/02_commute_economics.sql`

**Acceptance:** Compares wages with commute-cost burden; expected and experienced commute duration and expenses; fuel, toll, and parking contributions; cost bands; and interactions with shifts. Clearly distinguishes gross compensation after commute expenses from take-home pay.

### INV-03 Scheduling and flexibility

**Script:** `analysis/03_scheduling.sql`

**Acceptance:** Analyzes preferred versus assigned shifts, overnight schedules, weekend and holiday requirements, schedule changes, transfer availability, and combined schedule and commute burden. Preserves relevant schedule history.

### INV-04 Job experience and training

**Script:** `analysis/04_job_experience.sql`

**Acceptance:** Examines reported expectation alignment, experienced responsibilities, training consistency, conflicting instructions, onboarding feedback, and early exits. Uses dated reports and distinguishes unavailable responses from negative responses.

### INV-05 Career mobility

**Script:** `analysis/05_career_mobility.sql`

**Acceptance:** Distinguishes operational promotions, direct-hire conversions, lateral transfers, and advancement aligned or unaligned with recorded goals. Reports time to advancement and subsequent retention patterns, with comparisons between entry-level and experienced roles and explicit temporal limitations.

### INV-06 Combined retention patterns

**Script:** `analysis/06_combined_patterns.sql`

**Acceptance:** Investigates interacting factors such as commute and overnight work, commute costs and schedule mismatch, career expectations and mobility, and training and dissatisfaction. Uses stratification or comparable groups, includes positive retention patterns, and discusses confounding rather than ranking raw averages as causal effects.

### INV-07 Business impact and recommendations

**Script:** `analysis/07_business_impact.sql`

**Acceptance:** Quantifies replacement demand, recruiting and onboarding costs, early-turnover costs, and high-burden segments under documented cost definitions. Provides hypothetical intervention scenarios with explicit assumptions and avoids double-counting costs. Each recommendation links to findings and a measurable follow-up KPI.

### SQL-01 Meaningful advanced SQL

**Acceptance criteria**

- The investigations and reporting layer demonstrate multi-table joins, CTEs, conditional aggregation, CASE, ROW_NUMBER, RANK or DENSE_RANK, LAG, windowed aggregates, cohort calculations, date arithmetic, and segmentation.
- Correlated subqueries and transactions are used where justified by the problem; techniques are not inserted solely to satisfy a checklist.
- Views and parameterized stored procedures expose reusable reporting logic. Index choices support real access patterns.
- Significant queries explain the business question, result grain, and important correctness or performance decisions.

## 7 Performance engineering requirements

### PERF-01 Three measured optimization case studies

Complete three substantive cases using meaningful analytical queries. The handoff permits at least three; this delivery plan commits to three without adding extra cases by default.

**Acceptance criteria for each case**

- Preserve executable baseline and optimized SQL, relevant index definitions, and execution-plan evidence.
- Record SQL Server version, environment, dataset size, parameters, measurement procedure, repetition count, and cache conditions or limitations.
- Use `SET STATISTICS IO, TIME ON` and execution plans to collect actual logical reads and timing evidence before and after changes.
- Diagnose the observed issue and explain the chosen indexing or query changes and relevant tradeoffs.
- Verify equivalent results on the same data, including duplicate-row semantics where applicable.
- Report measured outcomes honestly, including mixed or negligible improvements. A fixed speedup percentage is not an acceptance requirement.
- Separate full local benchmark results from any smaller hosted-demo measurements. No benchmark figures are invented.

## 8 Dashboard requirements

### UI-01 Five required pages

The application is named **InnoStaff Workforce Intelligence**.

| Page | Required content |
|---|---|
| Executive Overview | Placement counts, retention KPIs, monthly trends, cohorts, and replacement demand |
| Commute & Scheduling | Commute burden and expectation gaps, shifts, weekend and holiday requirements, and schedule mismatch |
| Job Experience & Career Mobility | Training, expectation alignment, promotions, conversions, and career-goal alignment |
| Client & Role Explorer | Comparisons by client, site, role, branch, and cohort |
| Findings & Recommendations | Findings, high-burden segments, estimated costs, proposed improvements, and follow-up KPIs |

**Acceptance criteria**

- All five pages load and present the required information using SQL-backed results.
- Supported filters are defined in the dashboard design and return results consistent with direct SQL for the same parameters.
- Labels explain metric units and observation windows; rates have inspectable counts and denominators.
- Empty results and incomplete observations are handled clearly. Screenshots document the finished pages.
- Synthetic-data labeling and the distinction between findings and hypothetical scenarios remain visible where relevant.

### UI-02 SQL remains the analytical engine

**Acceptance:** Streamlit retrieves results through parameterized queries and reusable SQL Server views or procedures. Filter values are not concatenated into executable SQL. Pandas may format returned results and support charting but does not implement the core retention analysis.

## 9 Testing and reproducible operation

### QA-01 Automated verification

**Acceptance criteria**

- SQL and Python tests cover integrity, chronology, fixed-seed generation, known-answer aggregation and retention fixtures, and pre/post optimization equivalence.
- Tests include boundary cases and incomplete observations rather than relying exclusively on randomly generated data.
- GitHub Actions starts an isolated SQL Server environment, applies schema, loads deterministic small data, runs critical integrity checks and SQL/Python tests, and fails on critical errors.
- The final required CI run passes; instructions identify how to run the same checks locally.

### OPS-01 Local setup and credentials

**Acceptance criteria**

- A documented Docker Compose workflow starts SQL Server, applies schema, generates and loads a selected dataset size, validates it, and starts the dashboard.
- Setup is verified from an empty project database using documented prerequisites and commands.
- Configuration, supported environment, initialization order, and resource prerequisites are documented. Commands do not depend on undocumented manual data edits.
- Credentials are supplied through documented configuration or secrets and are absent from committed source. Example configuration contains placeholders.
- If a hosted demo is implemented, its setup, dataset differences, and access limitations are documented; database access is restricted appropriately.

## 10 Documentation and delivery evidence

### DOC-01 Required documentation

Maintain the agreed separate documents with depth appropriate to their purpose:

1. Requirements and Acceptance Criteria — this scope and completion baseline.
2. Database Design and Data Dictionary — ERD, schema definitions, and reasoning.
3. System Architecture — components and data-flow diagram.
4. Synthetic Data Specification — generation rules, assumptions, scale, and reproducibility.
5. Investigation Plan — questions, metrics, temporal rules, and expected output structures.
6. Testing and Performance Plan — fixtures, correctness checks, benchmark protocol, and environments.
7. Dashboard Design — lean mockup, page contents, filters, and interactions.
8. Development and Delivery Plan — implementation sequence, milestones, organization, and delivery approach.
9. Three optimization case studies — measured evidence and technical explanations.
10. Findings Report — answers to all seven investigations, recommendations, limitations, and future considerations.
11. README — business problem first, representative dashboard screenshot, overview, architecture, important decisions, setup, tests, and links to supporting evidence. Include deployment instructions if hosted.

**Acceptance:** Documents describe the implemented system accurately. Requirements link to relevant scripts, tests, screenshots, or reports in a lightweight completion checklist; a separate traceability system is unnecessary.

## 11 Definition of done

- [ ] Database design and data dictionary match the implemented schema.
- [ ] Integrity and historical consistency checks pass.
- [ ] Full synthetic dataset regenerates and loads successfully.
- [ ] All seven investigation scripts execute and have verified results.
- [ ] Retention calculations correctly handle threshold boundaries and incomplete follow-up.
- [ ] Three optimization case studies contain real measurements, plans, and equivalence evidence.
- [ ] All five dashboard pages and their documented filters work correctly.
- [ ] SQL remains the core analytical engine.
- [ ] Automated tests and GitHub Actions CI pass.
- [ ] Docker-based setup is verified and documented.
- [ ] Findings, recommendations, assumptions, and limitations are complete.
- [ ] README and screenshots make the work understandable and reproducible.
- [ ] No excluded features or real employer records have entered the project.

## 12 Review and change control

This document is a draft translating the approved handoff, not a claim that implementation or validation is complete. Review it before using it as the implementation baseline. Detailed design decisions may be resolved in the appropriate next document without expanding scope. Any material change to the seven investigations, three planned case studies, five pages, core stack, or exclusions must be explicitly recorded and agreed before implementation.
