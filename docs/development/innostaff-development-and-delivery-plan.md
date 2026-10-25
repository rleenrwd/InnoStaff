# InnoStaff Development and Delivery Plan

**Status:** Implementation roadmap. Repository and working branch exist; application development has not been claimed.

## Purpose and working method

Build the approved database-first project in small, explainable increments. Connect each implementation to the numbered requirements, explain important SQL decisions, and verify the result before moving forward. Documentation and tests evolve with the code rather than being reconstructed at the end.

Use working for development and preserve main as the release branch. Make focused commits when a meaningful piece works. Release sequencing is a presentation choice, not a reason to add artificial document dates or claim unfinished results.

## Repository structure

Keep these top-level areas and add internal folders only when contents justify them:

```text
InnoStaff/
  database/
  generator/
  analysis/
  dashboard/
  tests/
  performance/
  docs/
  scripts/
  .github/workflows/
  .env.example
  .gitignore
  docker-compose.yml
  requirements.txt
  README.md
```

Database scripts, generator code, and test entry points may start directly in their respective directories. All eight planning documents stay directly under docs/. The dashboard mockup is one companion HTML file. Do not create empty folder scaffolding for its own sake.

Use descriptive numbered SQL filenames when execution order matters, such as database/001_reference_tables.sql. The setup script declares the complete order; do not depend on filesystem enumeration. Keep investigation filenames fixed as specified in the requirements.

Ignore real .env files, generated datasets, local database volumes, virtual environments, Python caches, and temporary test output. Commit known-answer fixtures and selected benchmark evidence. No secrets belong in Git.

## Milestones and exit conditions

| Step | Work | Completion evidence |
|---|---|---|
| 1 Design review | Walk through requirements, ERD, time rules, and query needs | Documented decisions and consistent model |
| 2 Database foundation | Establish SQL Server environment; implement reference and placement tables, constraints, historical records | Schema creates in an empty database; representative valid/invalid cases verified |
| 3 Small data and checks | Implement generator and loader; add known-answer fixtures and early tests | Deterministic small load and exact metric checks |
| 4 Full data | Extend scenarios and scale to full profile | Manifest, valid row counts, successful full load |
| 5 Seven investigations | Implement in numbered order, sharing metric definitions | Verified query outputs and documented limitations |
| 6 Performance cases | Profile real queries and complete three optimizations | Plans, raw measurements, equivalence evidence |
| 7 Reporting and dashboard | Expose SQL views/procedures and build five pages | Filtered SQL/UI agreement and screenshots |
| 8 Delivery rehearsal | Finish CI, Compose packaging, README, and findings | Passing CI and clean setup rehearsal |

Introduce tests and a minimal CI workflow during steps 2–3. Extend them as tables and queries are added; step 8 is final verification rather than the first testing effort.

## First implementation sequence

1. Place the planning files directly under docs/ and review the example worker journey against the ERD.
2. Establish a tested SQL Server container and a connection using the selected local SQL tool.
3. Implement the first small group of reference tables, explaining their keys and constraints.
4. Insert a few known valid records and demonstrate a rejected invalid reference.
5. Expand incrementally into placements and their historical child records.

Do not generate every application file before these foundational decisions are understood. Version pinning and exact commands are finalized once the environment is exercised.

## Setup and loading contract

The final setup script or documented command sequence must start SQL Server, wait for query readiness, apply scripts, generate a chosen profile, load it, validate it, and start Streamlit. It must clearly identify the target database and stop on errors.

Default setup does not destroy an existing database. Resetting a demonstration database is a separate explicit action. Fresh initialization and reloading must not silently append duplicate records. Mark data ready only after cross-table checks pass; dashboard startup must not suggest a partial load is complete.

The precise shell/Python entry-point names are chosen during implementation and then recorded in the README. This roadmap does not present unimplemented commands as working setup instructions.

## Performance and evidence packaging

Create performance/case-01 through case-03 only when selecting cases. Keep each baseline, optimized query, plan, measurements, and narrative together. The case study explains the problem, evidence, diagnosis, change, correctness check, outcome, and limitations.

The findings report is written from validated outputs after all seven investigations. It must identify dataset revision, parameters, population, and script for each major claim. Screenshots are captured from the implemented dashboard, not from planning mockups.

## Documentation release grouping

The user may release the documents in two equal groups without adding dates:

| Group | Planning documents |
|---|---|
| First half | Requirements and Acceptance Criteria; Database Design and Data Dictionary; System Architecture; Synthetic Data Specification |
| Second half | Investigation Plan; Testing and Performance Plan; Dashboard Design; Development and Delivery Plan |

Publish the HTML mockup alongside Dashboard Design. The planning set has no publication dates. Git history records when files are committed; any release description should accurately call these design documents, not completed implementation.

## Final delivery and optional hosting

The README begins with the fictional business problem and includes a real dashboard screenshot, architecture overview, exact tested setup and test commands, dataset regeneration, seven investigation links, three performance case links, limitations, and a documentation index.

A read-only hosted demo is optional after local completion. Azure SQL can use smaller representative data if disclosed. Do not let hosting work expand the core scope or delay a complete local project.

Completion uses the checklist in [Requirements and Acceptance Criteria](innostaff-requirements-and-acceptance-criteria.md). Update it with actual evidence links as implementation progresses. No milestone is marked complete simply because its plan exists.
