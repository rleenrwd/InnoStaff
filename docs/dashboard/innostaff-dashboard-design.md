# InnoStaff Dashboard Design

**Status:** Presentation design baseline. Mockups contain no real query results.

## Purpose and visual direction

InnoStaff Workforce Intelligence presents the seven SQL investigations through five lightweight Streamlit pages. It is a read-only portfolio demonstration, not an operational staffing portal.

Use a restrained workforce-reporting style: warm white background, dark navy text/navigation, teal primary charts, muted amber for limitations, and clear tables. Color is accompanied by labels rather than used as the only indicator. Use native Streamlit controls and charts; do not spend scope recreating a custom frontend framework.

The companion [five-page mockup](innostaff-dashboard-mockups.html) provides concrete page composition, sidebar controls, cards, charts, and evidence sections. It is a static design artifact with page navigation only. Every displayed measure is a placeholder, and the decorative chart shapes are labeled illustrative.

## Shared shell and controls

The sidebar contains the five page links and a compact filter form. The main header identifies the current page, dataset profile, and fictional-data status. A context line states the placement start range, analysis cutoff, primary population, and selected retention horizon.

| Control | Behavior |
|---|---|
| Placement start range | Inclusive start and exclusive end; limits the placement population |
| Analysis cutoff | No later than SnapshotDate; excludes future observations |
| Role level | Defaults to Entry Operations; supports explicit comparison populations |
| Client | Optional single-client filter |
| Site | Optional, restricted to selected client where one is selected |
| Recruiting branch | Optional historical order ownership |
| Hiring cohort | Optional operational intake cohort |
| Retention horizon | 30, 60, or 90 days, default 90 |
| Apply filters | Submits one consistent parameter set |

Changing a client clears an incompatible site or cohort. Keep submitted parameters across pages. Reset restores default Entry Operations population, full available placement-start range, snapshot cutoff, and 90 days. No need to add exports, uploads, user management, or saved dashboards.

Use one selection per dimension initially; multi-select lists are unnecessary for approved comparisons. The explorer can group across all clients or sites with the corresponding filter unset. Labels distinguish overall worker count from placement count.

## Page 1 Executive Overview

**Sources:** INV-01 and replacement-demand outputs from INV-07.

Top row: placement count, selected-horizon retention, eligible placements, and replacement starts. The retention card includes numerator and denominator. Below, show a cohort-start-month retention trend and an operational hiring-cohort comparison. A hiring-purpose chart separates growth, replacement, and transfer.

The page ends with a compact data-coverage table showing incomplete windows, early exits by class, and the selected population. Trends display unavailable immature months as gaps rather than zero retention.

## Page 2 Commute and Scheduling

**Sources:** INV-02 and INV-03.

Use two tabs or sections within this page, not new application pages. Commute shows median burden among observed assessments, paired expected/experienced coverage, cost-band retention, and commute-time gaps. Scheduling shows initial preference mismatch, assigned shift comparisons, weekend/holiday requirements, and request outcomes.

An interaction table compares commute burden and shift within comparable groups. Explain when a chart uses baseline estimates versus day-14 survivors. Never place their percentages side by side without naming their populations. Cost labels say USD/month or share of gross compensation.

## Page 3 Job Experience and Career Mobility

**Sources:** INV-04 and INV-05.

The training section shows first-week coverage, completion, reported conflicts, and day-7-to-day-30 outcomes. Survey charts use day-14 respondents and show low, neutral, high, and unknown categories.

The mobility section shows promotions, conversions, transfers, time to observed first advancement, and goal alignment. Clearly separate event counts from the day-180-to-day-270 internal-promotion comparison. Explain that client employment after conversion is not observed.

Show response and landmark inclusion counts next to conclusions so readers can see who was excluded.

## Page 4 Client and Role Explorer

**Sources:** INV-01, INV-05, INV-06.

Provide a grouping selector for client, site, role, recruiting branch, or hiring cohort. Use allowlisted SQL grouping options. Show a comparison chart and a sortable result table with placement count, eligible count, retained count, rate, voluntary-exit count, and a small-sample indicator.

Default ordering is eligible placement count descending rather than an unsupported “best employer” ranking. An optional rate sort is descriptive. Small groups remain visible with a warning and are omitted from recommendation rankings.

## Page 5 Findings and Recommendations

**Sources:** INV-06, INV-07, and the final findings report.

Show evidence-backed findings with links to the relevant investigation, cohort, and limitations. A business-impact section presents recruitment/training cost definitions, replacement demand, and high-burden segments.

A compact scenario form accepts an assumed absolute retention improvement of 0–10 percentage points and a nonnegative total intervention cost for the same filtered cohort. Default improvement is zero. SQL computes avoided exits and gross/net modeled benefit; cap the modeled improvement to the selected cohort's relevant eligible exit percentage so avoided exits cannot exceed qualifying exits.

Label scenario figures “Hypothetical” wherever shown. Negative net benefit remains visible. Recommendations include an owner category such as Recruiting or Client Operations, an action, linked evidence, and a follow-up KPI. These are hypothetical operational recommendations, not messages sent to real organizations.

## Output and interaction rules

- Retention rates always expose counts and the horizon. Empty eligible sets show Not available.
- Show Unknown for missing answers or alignment. Do not silently omit missing groups.
- Use plain language such as “associated with” rather than causal assertions.
- Tables use readable currency/percentage formatting; underlying SQL retains precision.
- Charts show counts or percentages explicitly, with concise titles and text interpretation.
- A database error gives a short safe message without connection strings or SQL secrets.
- If caching is enabled, the key includes submitted parameters and dataset identity.
- Explain the sampled attendance scope anywhere those data appear; no full-workforce absence claim.

## Implementation and acceptance

Use Streamlit navigation and five page modules, plus a small shared connection/query helper. Pandas may format or chart results; metric logic stays in SQL Server. Select chart types supported by the chosen library, favoring line charts for trends and bars/tables for comparisons.

The page is complete when required data render, two parameter sets match direct SQL, empty and incomplete cases behave correctly, and a readable screenshot is captured. The mockup is a design reference; its chart shapes are not evidence of a finding.

Reference: [Streamlit multipage navigation](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation).
