# InnoStaff Testing and Performance Plan

**Status:** Planned verification. No tests or benchmarks have been executed.

## Purpose

Verify database integrity, analytical correctness, reproducible data, and honest performance evidence. Tests focus on failure-prone business rules and independently known answers. Full-size benchmarks demonstrate local SQL engineering; CI verifies correctness on small data.

Requirements are defined in [Requirements and Acceptance Criteria](innostaff-requirements-and-acceptance-criteria.md). Metric semantics are defined in [Investigation Plan](innostaff-investigation-plan.md).

## Test environments and layers

| Layer | Data | Main purpose | Required evidence |
|---|---|---|---|
| Python unit checks | Small constructed records | Determinism, ranges, chronology helpers | Automated pass/fail |
| SQL known-answer tests | Hand-authored fixture | Exact retention, cost, temporal-join results | Expected versus actual rows |
| Database integration | Small generated profile | Complete schema/load/reporting path | Validation report and CI log |
| Dashboard smoke checks | Small or full profile | Five pages and parameter consistency | Manual checklist and screenshots |
| Performance | Frozen full profile | Three measured query cases | Raw metrics, plans, equivalence results |
| Clean setup rehearsal | Empty disposable database | Reproducible delivery | Commands and outcome recorded |

Pin tested SQL Server image, compatibility level, Python version, database driver, and dependencies during setup. Record actual versions after execution. A design document is not evidence that a configuration works.

## Integrity tests

| ID | Condition | Expected behavior |
|---|---|---|
| INT-01 | Orphan FK, duplicate unique code, duplicate attendance day | SQL statement rejected |
| INT-02 | Negative wage/cost, score 0 or 6, unsupported status | Constraint rejects row |
| INT-03 | End before/on start, invalid request shape | Constraint rejects row |
| INT-04 | Placement cohort belongs to another order | Cross-table validation fails |
| INT-05 | Schedule gaps or overlaps, request with wrong parent placement | Validation fails |
| INT-06 | Attendance or survey outside placement interval | Validation fails |
| INT-07 | Career event after source end or before source start | Validation fails |
| INT-08 | Goal belongs to another worker or is future-dated | Validation fails |
| INT-09 | Ended placement missing exit, active placement with exit | Validation fails |
| INT-10 | Replacement self-link, cycle, duplicate vacancy successor, wrong site/role | Validation fails |
| INT-11 | Previous placement belongs to another worker or overlaps | Validation fails |
| INT-12 | Transfer marked agency departure, conversion classification inconsistent | Validation fails |

Tests distinguish engine-enforced rules from validation-enforced rules. Valid setup must run both; a passing insert alone is not proof of valid business data. Invalid-data tests run in transactions or isolated databases so the test environment is recoverable.

## Exact retention fixture

Use AsOfDate 2026-04-01 and StartDate 2026-01-01 for A through D. EndDate is exclusive.

| Placement | EndDate | 30-day result | 60-day result | 90-day result |
|---|---|---|---|---|
| A | NULL | Retained | Retained | Retained |
| B | 2026-01-11 | Not retained | Not retained | Not retained |
| C | 2026-01-31 | Not retained at boundary | Not retained | Not retained |
| D | 2026-03-02 | Retained | Not retained at boundary | Not retained |
| E, starts 2026-03-20 | NULL | Incomplete | Incomplete | Incomplete |
| F, starts 2026-03-20 | 2026-03-25 | Incomplete, known early exit | Incomplete | Incomplete |

Expected eligible denominator is 4 for each horizon. Retained counts are 2, 1, and 1. Rates are 50%, 25%, and 25%. E and F are excluded consistently from those denominators and counted as incomplete windows.

Add a separate G ending exactly on day 90 to assert that boundary directly. Add a worker with multiple placements to prove that placement count and distinct-worker count are different. With AsOfDate earlier than an eventual EndDate, assert that future exit information does not change historical active status.

Other fixtures verify zero eligible denominator returns NULL; subgroup total recomputation uses counts; conversion and transfer end a placement but remain separately classified; and NULL EndDate is not a guarantee of complete follow-up.

## Analytical test cases

- A placement with two surveys, three training sessions, and two commute observations still contributes one placement to a retention group.
- A survey on day 20 cannot affect a day-14 grouping. A promotion on day 240 cannot affect the day-180 promoted group.
- A person leaving before day 7 is reported outside the training landmark rather than mislabeled as a trained survivor.
- A denied shift request does not change the effective schedule; a request resolved after the analytical cutoff is still pending at that cutoff.
- Expected USD 10/day × 5 days/week and USD 25/hour × 40 hours/week produce monthly costs 216.6667 and gross 4,333.3333 before display rounding, for 5% burden. No extra factor of two is applied to daily costs.
- Exactly 5%, 10%, and 15% enter the next burden band. Missing assessments produce Unknown, not zero burden.
- One recruitment cost of USD 500 and two training costs of USD 100 produce USD 700 onboarding cost. A linked replacement's costs are not duplicated through joins or combined with predecessor costs as the same measure.
- A scenario with zero assumed improvement has zero gross savings; nonzero intervention cost can make net benefit negative.
- Grouping by site can reverse an overall association in a constructed example. The report must preserve the strata and avoid a causal conclusion.

Fixtures are committed with independently specified expected rows. Do not generate expected answers by invoking the same production calculation under test.

## Generator tests

Generate the small profile twice with identical seed, configuration, code, and dependency versions; compare canonical per-table hashes excluding runtime metadata. Verify requested reference counts, relationship validity, no future records, sampled attendance uniqueness, positive/neutral/negative cases, and required retention windows.

Test at least one different seed to ensure it changes logical records while preserving integrity. Validate impossible configuration with a clear error rather than silently clipping all outcomes. Full-profile generation and loading are separate acceptance checks, not required on every CI run.

## CI sequence

1. Check out source and install pinned dependencies.
2. Start isolated SQL Server and wait for a successful query, not merely an open port.
3. Apply schema, constraints, indexes, views, and procedures in declared order.
4. Load the known-answer fixture and run exact SQL correctness tests.
5. Reset the disposable test database, generate/load the small profile, and run integrity and report integration checks.
6. Run Python tests and deterministic generation checks.
7. Publish diagnostic logs on failure without connection secrets; return a nonzero exit code for critical failures.

Do not add timing thresholds to shared-runner CI. Preserve enough logs to identify the failing test and SQL error. Tests and setup scripts explicitly target test databases.

## Three optimization cases

Choose final queries after profiling. Initial candidates are cohort retention with selective start filters; latest eligible commute/survey selection over one-to-many histories; and cost aggregation joining placements with training or replacement chains. Do not manufacture an artificially bad query solely to obtain a large speedup.

Each case lives in performance/case-01, case-02, or case-03 and contains baseline.sql, optimized.sql, relevant index changes, before/after .sqlplan files, raw statistics logs, measurements.csv, and a written case study. Final selected queries must answer a real approved question.

### Measurement protocol

1. Freeze the full dataset and record manifest hash, code revision, SQL Server build/edition, compatibility level, container limits, host CPU/memory/storage, row counts, existing indexes/statistics, and database settings.
2. Choose representative fixed parameters plus at least one different selectivity. Use the same data and parameters before and after a change.
3. Run a baseline correctness check. Enable SET STATISTICS IO ON and SET STATISTICS TIME ON, and capture an actual execution plan using supported SQL tooling.
4. Capture diagnostic plans separately from primary timing runs, or apply identical plan-capture settings to both variants. State the method because instrumentation adds overhead.
5. Use one untimed warm-up then at least five timed executions for each variant/parameter set. Alternate baseline and optimized measurements where the change permits; for index changes requiring separate states, measure separate documented blocks and repeat if environmental load differs materially.
6. Record each run, not just the fastest. Report median elapsed and CPU time, logical reads by relevant object, ranges, result row count, and plan warnings or spills. Separate compile from execution time.
7. Apply a diagnosed change, repeat under comparable conditions, and verify result equivalence.

Warm-cache testing is the default. Do not run cache-clearing commands against shared or non-test environments. If an isolated cold-cache experiment is justified, label it separately and document precisely what was cleared. No dashboard cache or Python rendering time is part of engine-query measurements.

### Equivalence and interpretation

Compare expected columns, values, NULL behavior, counts, and duplicate multiplicities. Two-way EXCEPT can establish set equivalence but misses duplicate-count differences; compare grouped full-row multiplicities or keyed records as well. Ordering is only part of correctness when ORDER BY is in the output contract.

Report percentage reduction only when the baseline is positive: 100 × (baseline minus optimized) / baseline. A faster plan on one parameter set may be worse on another. Explain index storage/write costs and parameter sensitivity where observed. Operator cost percentages are optimizer estimates, not measured wall-clock shares.

No minimum speedup is required. If a proposed optimization does not help, preserve the result and either explain the tradeoff or select another genuinely useful case. Complete three evidence-backed cases; do not publish unsupported claims.

## Dashboard and release checks

For each page, compare at least one unfiltered and one filtered result against direct SQL with identical parameters. Check empty results, small samples, incomplete windows, historical cutoffs, persistent filters, cache invalidation after data reload, and safe database errors.

Verify screenshots have no credentials or real personal data. Rehearse setup from an empty disposable database and confirm all seven scripts and five pages run. The final README records actual commands and tested versions, replacing any planned command names.

## Primary technical references

- [Microsoft SET STATISTICS IO](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-statistics-io-transact-sql)
- [Microsoft SET STATISTICS TIME](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-statistics-time-transact-sql)

These document the diagnostics selected for this project. The benchmark protocol above is the project's planned method, not a statement that results already exist.
