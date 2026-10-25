# InnoStaff Synthetic Data Specification

**Status:** Generator design baseline. No generated results exist yet.

## Purpose and authenticity

Generate a fictional Bay Area staffing history that supports all seven investigations and meaningful query optimization. Geographic labels may refer to public regions; clients, workers, trainers, costs, assignments, and outcomes are invented. Do not import employer records, personal information, proprietary practices, or real-company names.

Every finding must be described as a property of this generated dataset. The generator intentionally creates relationships; discovering one does not independently validate a real-world explanation.

## Snapshot and profiles

Use a configured SnapshotDate rather than the current machine date. The default snapshot spans 36 complete calendar months, from 2023-10-01 through 2026-09-30 inclusive. SnapshotDate is 2026-09-30. These are dataset coverage parameters, not document publication dates. Do not generate records after the cutoff.

| Profile | Workers | Placements | Attendance | Clients | Purpose |
|---|---:|---:|---:|---:|---|
| Full | 25,000 | 60,000 | About 750,000 | About 150 | Portfolio analysis and local benchmarks |
| Small | 250 | 600 | About 7,500 | 10 | CI integration and development |
| Known answer | Small hand-authored set | Explicit cases | Explicit cases | Few | Exact metric and boundary assertions |

The full and small profiles use the same generation rules, scaled counts, and fixed seed 41027. They are not required to be subsets of one another. Exact reference counts, dependency versions, configuration, and actual produced counts go into a manifest. If feasible attendance days cannot meet the target, record the actual count instead of duplicating days or violating timelines.

## Configuration and reproducibility

Keep one versioned configuration per profile containing seed, date bounds, row targets, role mix, score and missingness rules, probability coefficients, cost ranges, and scenario toggles. Use a dedicated random-number generator rather than uncontrolled global randomness. Allocate separate deterministic random streams to major entities so a new survey field does not unexpectedly rewrite the client population.

Sort output by stable primary key and use explicit ISO dates, UTF-8 text, decimal rounding, and stable NULL representation. Pin generator dependencies once implemented. Identical seed, configuration, generator revision, and dependency environment must reproduce the same logical records and canonical output checksums. Reproducibility is not promised across arbitrary library upgrades.

The manifest records generator revision, seed, profile, coverage, canonical configuration hash, per-table row counts, file hashes, and validation results. Runtime timestamps, if captured for troubleshooting, are excluded from logical reproducibility comparisons. Generated files and manifests remain ignored local output; publish the small fixture and useful run summaries, not hundreds of thousands of generated CSV rows in Git.

## Generation order

1. Create fictional clients, sites, branches, recruiters, and role definitions.
2. Create workers and dated career goals.
3. Create job orders and cohorts with frozen advertisement details.
4. Allocate placements, wages, historical schedules, and vacancy chains.
5. Draw employment outcomes using the disclosed synthetic model.
6. Create valid commute observations, training, surveys, requests, attendance, exits, and career events within those timelines.
7. Validate relationships and chronology, write stable output and a manifest, and load SQL Server in dependency order.

In step 5, use initially assigned exposures for the primary outcome model. Later experience scores may be correlated with those exposures but must not secretly use future exit labels as inputs. Any intentional response-selection mechanism must be disclosed.

## Population and scenario rules

The following are proposed initial synthetic settings, not claims about actual staffing work. Tune them for adequate analytical coverage before freezing the first published dataset; retain the final settings and revision in the manifest.

| Dimension | Initial generation rule |
|---|---|
| Role mix | About 70% entry operations, 20% intermediate operations, 10% experienced technical placements |
| Regional distribution | Multiple sites across SF, peninsula, South Bay, and East Bay; uneven hiring volumes |
| Workers | Mix of prior gig, operations, technical, and other backgrounds; some never placed |
| Placements per worker | Skewed distribution allowing repeat placements; no overlapping assignments per worker |
| Cohorts | Unequal intake sizes, repeated cohorts for high-volume orders, some individual starts |
| Wages | Broad fictional bands: entry USD 23–38/hour, intermediate 30–55, experienced 45–100 |
| Contract hours | Mostly 32–40/week; some 20–30; never inferred from attendance sampling |
| Commutes | Mix of short and long journeys; positive regional/site relationships with noise |
| Expectations | Prestart estimates plus later observations; both underestimates and overestimates |
| Schedules | Day, swing, overnight, rotating; a mixture of matched and mismatched preferences |
| Training | Consistent and inconsistent sessions, multiple trainers, missing feedback, varying completion |
| Career goals | Technical advancement, operations advancement, stability, and other goals |
| Mobility | Promotion, lateral movement, conversion, no event, and unknown target alignment |
| Outcomes | Active placements and several exit classes; some long-tenure workers even in high-burden groups |

Use conditional probabilities rather than hard rules such as “all overnight workers leave.” Introduce client/site and cohort differences, worker-level variation, calendar variation, and random noise. Experienced roles generally have better retention in this fictional setting, with overlapping outcomes across categories.

## Synthetic turnover mechanism

Use a discrete monthly or weekly exit-hazard model, documenting the chosen interval before generation code is finalized. Baseline hazard varies by role level and tenure band. Commute burden, schedule mismatch, and inconsistent onboarding may increase risk probabilistically; supportive conditions and stable-employment preference may decrease it. A modest interaction between commute burden and overnight work provides an interaction example.

Draw an exit opportunity from the configured hazard; separately classify voluntary, involuntary, and planned endings using documented probabilities. Contract completion, conversion, and transfer must not all be encoded as dissatisfaction. Keep time available for active placements near the snapshot cutoff, producing incomplete retention windows.

Publish the final coefficients, baseline probabilities, and drawing sequence alongside the generator. They are parameters of a simulation, not fitted real-world estimates. Inspect distributions for accidental all-or-nothing relationships. Do not repeatedly regenerate seeds to get an impressive finding.

## Timeline and historical rules

Workers register before their first placement. Job orders open before placement starts. Cohorts belong to their orders. Placement end dates are exclusive. Events and assessments obey the dictionary's date bounds.

Create an initial expected commute assessment no later than start. Experienced assessments and survey responses begin only after work starts. Keep goal observations available before events where alignment is meant to be known; intentionally missing goals produce Unknown alignment. Approved schedule requests lead to new nonoverlapping effective schedule intervals. Denied requests preserve the old schedule.

A replacement links to an ended vacancy at the same role and site, with no branching duplication. Replacement starts after or on the prior end date. A transfer can link the same worker's consecutive placements. No cycles or self-links are allowed. AgencyDeparture is explicitly generated; it is not inferred from silence after an assignment.

## Attendance sampling

About 750,000 records cannot represent every workday across all 60,000 placements over three years. Attendance is therefore a sampled panel of scheduled workdays.

Construct feasible workdays for each placement from its effective schedule. Sample days using a fixed-seed rule and a bounded per-placement allocation, then sample additional feasible days to approach the global target. Do not sample the same placement/day twice. A missing workday is unobserved, not absent.

Attendance summaries describe observed days only and include coverage counts. Attendance is not used to calculate total wages, complete staffing utilization, or total absence prevalence across unobserved days. Commute economics uses contractual hours and assessed commute days instead.

## Missingness and positive patterns

Proposed initial response availability is about 80% for early experienced commute assessments, 65% for an early worker survey, and 75% for a pre-event usable career goal. Actual availability depends on time employed; someone leaving before a planned response cannot complete it. Optional survey questions may also be unanswered.

Document response opportunities and missingness by tenure, role, and outcome. Availability is not independent of retention, so landmark analyses state the population they actually represent. Do not impute a positive or negative response for silence.

Include satisfied long-tenure workers, manageable high-wage and low-wage commutes, preferred overnight schedules, successful operations careers, and technical advancement. At least one plausible proposed relationship should be weak or mixed in the final generated sample; report whatever appears rather than forcing an analytical conclusion.

## Cost assumptions

RecruitmentCostUSD is an invented nonnegative recruiting cost recorded per placement. TrainingCostUSD is an all-in session cost including delivery and trainee paid training time. Their definitions are disjoint. No additional training-wage line is added later.

Initial configured ranges may be USD 200–1,500 per recruitment and USD 50–600 per training session. Publish final ranges and distributions. All financial outputs are synthetic modeled costs. Hypothetical retention scenarios use separately supplied improvement assumptions, not a claim that changing schedules or paying a stipend guarantees a particular improvement.

## Generator acceptance

Generation passes only when all keys, row-level ranges, cross-table consistency, and chronology checks pass. Compare repeated outputs by logical record hashes. Verify presence of all required categories and enough eligible observations for all three retention horizons and the career-mobility landmark. Record insufficient segments transparently rather than adding fake records to satisfy a chart.

Full data loading and benchmark execution remain future implementation steps. See [Testing and Performance Plan](../testing/innostaff-testing-and-performance-plan.md).
