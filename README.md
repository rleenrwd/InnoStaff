# InnoStaff Workforce Solutions

InnoStaff is a fictional Bay Area staffing agency investigating early turnover in high-volume technical-operations placements. This portfolio project uses SQL Server database engineering, reproducible synthetic workforce data, seven SQL investigations, three measured optimization case studies, and a lightweight Streamlit dashboard.

**Current stage:** Documentation and implementation design. The database, generator, investigations, performance results, and dashboard are not implemented in this package.

## Project focus

The primary questions concern 30/60/90-day placement retention, commute economics, schedule fit, onboarding, job expectations, career mobility, and replacement hiring costs. The engineering focus is relational modeling, historical correctness, advanced SQL, data integrity, and reproducible query-performance evidence.

All business records are fictional. Any later findings describe the synthetic dataset, not real employers. Optional hosting does not change the local completion requirements.

## Documentation

| Document | Purpose |
|---|---|
| [Requirements and Acceptance Criteria](docs/requirements/innostaff-requirements-and-acceptance-criteria.md) | Scope and verifiable completion conditions |
| [Database Design and Data Dictionary](docs/database/innostaff-database-design-and-data-dictionary.md) | ERDs, 17-table model, fields, constraints, history |
| [System Architecture](docs/architecture/innostaff-system-architecture.md) | Components, data flow, analytical responsibilities |
| [Synthetic Data Specification](docs/synthetic-data/innostaff-synthetic-data-specification.md) | Dataset profiles, generation assumptions, reproducibility |
| [Investigation Plan](docs/investigations/innostaff-investigation-plan.md) | Seven questions, metric formulas, time-aware comparisons |
| [Testing and Performance Plan](docs/testing/innostaff-testing-and-performance-plan.md) | Fixtures, CI, benchmark protocol, correctness evidence |
| [Dashboard Design](docs/dashboard/innostaff-dashboard-design.md) | Five pages, filters, chart contents, interaction rules |
| [Development and Delivery Plan](docs/development/innostaff-development-and-delivery-plan.md) | Incremental implementation and release evidence |

Open [Dashboard Mockups](docs/dashboard/innostaff-dashboard-mockup.html) locally in a browser to review all five layouts using the navigation links. The static mockups contain placeholders and illustrative chart shapes, not findings. GitHub may display the HTML source rather than render it.

## Planned stack and organization

SQL Server performs the analysis. Python generates data and supports orchestration. Streamlit presents SQL results. Docker Compose supports local setup, and GitHub Actions verifies correctness on a small deterministic dataset.

Implementation will use `database/`, `generator/`, `analysis/`, `dashboard/`, `tests/`, `performance/`, and `scripts/`, with subfolders organized by responsibility. Planning documents are grouped into their corresponding subfolders under `docs/`.

## Reproducing the finished project

Executable setup and test commands will be documented here after the environment and scripts are implemented and exercised. This documentation package is not an executable application release. Do not treat mockup figures or planned benchmark procedures as completed results.

The finished README will add actual dashboard screenshots, tested setup commands and versions, findings, and links to all three measured optimization cases. Scope exclusions and the completion checklist are maintained in the requirements document.
