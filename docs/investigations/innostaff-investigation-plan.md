# InnoStaff Investigation Plan

**Status:** Analytical design baseline. Findings are not yet available.

## Purpose and analytical population

Implement exactly seven investigations, each answering an approved business question through SQL Server. The primary population is entry-level Operations placements; intermediate and experienced roles are explicit comparison populations. Do not silently combine them into a claim about entry-level turnover.

The unit of retention is a placement, not a person, attendance row, survey, or training session. Repeated placements by the same worker are legitimate records but are not independent people. Always label counts accordingly and disclose this limitation.

The parameter AsOfDate is an inclusive calendar cutoff no later than the generated dataset SnapshotDate. PlacementStartFrom is inclusive and PlacementStartTo is exclusive. Other filters identify client, site, role level, recruiting branch, and cohort. Filter placement starts first; dated observations are then restricted to the correct placement and observation time. Job-order recruiter and branch are historical attribution.

## Shared metric contract

### Placement retention

For horizon H in {30, 60, 90}, define ThresholdDate = StartDate + H calendar days.

- Eligible: ThresholdDate <= AsOfDate.
- Retained: eligible and EndDate is NULL or EndDate > ThresholdDate.
- Not retained: eligible and EndDate <= ThresholdDate.
- Incomplete window: ThresholdDate > AsOfDate, shown outside the rate denominator even if an early exit is already known.
- Retention percentage: 100 × retained count / eligible count. A zero denominator yields NULL and displays “Not available,” not 0%.

This measures active placement status on day H after start. EndDate is the first inactive date, so ending exactly on ThresholdDate is not retained. This definition deliberately uses mature start cohorts for comparable rates. An early exit in an immature cohort is a known exit but is not added selectively to that horizon's denominator.

Return placement_count, eligible_count, retained_count, not_retained_count, incomplete_window_count, and retention_percent for every retention row. Use exact numeric arithmetic before rounding only for display. A placement ending after AsOfDate is treated as still active at that cutoff. Never filter historical reports solely by the snapshot PlacementStatus field.

The primary rate is all-cause placement retention: conversion, transfer, contract completion, voluntary exit, and involuntary exit can all end a placement. Separately return exit-class counts and voluntary early-exit percentage using the same eligible denominator. A conversion may be a positive career outcome despite lowering placement retention. Never rename all-cause nonretention “dissatisfaction.”

### Cohorts and grouping

Monthly hiring cohorts are placement-start calendar months, distinct from operational HiringCohortId intake groups. Both are reportable and labeled. Trends use cohort month for retention and event month for exit or recruitment flows; these series must not share an ambiguous “month” heading.

Return group sample counts. For segments with fewer than 30 eligible placements, label the estimate “Small sample” and omit rank-based recommendations. This is a presentation threshold, not a statistical significance test. Aggregated totals are recomputed from summed counts rather than averaged percentages.

### Selecting dated observations

Choose one applicable observation per placement using ROW_NUMBER ordered by observation date descending, then primary key descending. Aggregate training sessions and attendance separately before joining. Never multiply placement rows by joining raw surveys, sessions, goals, and attendance simultaneously.

Prestart expected commute: latest Expected assessment on or before StartDate. Initial schedule: effective Schedule row containing StartDate. Requests never count as schedule coverage. Career goal at an event: the referenced latest goal known on or before that event, validated against the worker.

Experienced measurements cannot explain first-day outcomes. Use prespecified landmark cohorts:

| Question | Landmark | Measurement window | Subsequent outcome |
|---|---|---|---|
| Early training and first-month exits | Start + 7 days | Start through day 7 | Active on day 30 |
| Experienced commute, schedule fit, surveys | Start + 14 days | Start through day 14 | Active on day 90 |
| Internal promotion and later retention | Start + 180 days | Start through day 180 | Active on day 270 |

Landmark eligibility requires active placement on the landmark and sufficient observation opportunity to the final horizon. Comparisons only use measurements known by the landmark. Separately report placements lost before the landmark, missing measurements, and included counts. These results describe landmark survivors and respondents, not every original hire.

For career comparisons, promotion status is fixed at day 180; a day-240 promotion cannot retroactively enter the promoted group. Conversions and transfers that ended a source placement before day 180 are reported as separate events, not excluded evidence of poor careers. This simple fixed-landmark approach limits time-related bias but does not establish causation.

### Commute economics

All costs are estimated USD. Monthly gross compensation = HourlyWage × ContractWeeklyHours × 52 / 12. Monthly commute expense = (FuelDailyUSD + TollsDailyUSD + ParkingDailyUSD) × CommuteDaysPerWeek × 52 / 12.

Commute burden percentage = 100 × monthly commute expense / monthly gross compensation. Daily costs already represent the round trip and are not doubled. Round-trip time = 2 × OneWayMinutes. Expected/experienced gap = experienced minus expected on the same units.

Use burden bands below 5%, 5–under 10%, 10–under 15%, and 15% or higher. One-way time bands are under 30, 30–under 60, 60–under 90, and 90+ minutes. Boundaries are tested. Values missing either component remain Unknown for gap analysis. Gross compensation less commuting expense is not net take-home pay.

### Experience and alignment

Survey scores 1–2 indicate low fit, 3 neutral, and 4–5 high fit; NULL is Unknown. Use the latest eligible response by the landmark, with question-specific denominators. StableEmploymentPreferred is a separate reported preference.

At a career event, technical or operations goal alignment compares the target role family with the recorded goal family. Unknown target or goal remains Unknown. Stability goals are reported separately. Text descriptions provide context; no NLP, AI, or subjective automatic classification is required.

## Investigation 1 Retention baseline and hiring cohorts

**Script:** analysis/01_retention_baseline.sql  
**Requirements:** INV-01, AN-01

Report counts and 30/60/90-day rates overall and by role level, role, client, site, operational cohort, and monthly cohort. Use LAG to show percentage-point changes in comparable monthly rates, with NULL when comparison is unavailable. Use window aggregates for share of placement volume and DENSE_RANK for sufficiently sized client/site groups, with deterministic tie display.

Report Growth, Replacement, and Transfer starts separately. Replacement count comes from explicit HiringPurpose and a validated vacancy link, never from guessing that a new hire follows an exit.

**Outputs:** retention summary at one row per segment and horizon; cohort trend; hiring-purpose counts.  
**Verification:** known-answer fixture rates, consistent denominators, no duplication from joins, totals reconcile with placement counts.

## Investigation 2 Commute economics

**Script:** analysis/02_commute_economics.sql  
**Requirements:** INV-02, AN-02

Compare baseline expected burden with 30/60/90-day retention for mature cohorts. For experienced burden and mismatch, use the day-14-to-day-90 cohort. Show wages, component expenses, duration, burden bands, matched expected/experienced counts, and shift interactions.

Stratify within role level and site or client before describing wages versus commuting burden. The project can compare observed associations; it does not establish that burden “explains more” through an unimplemented predictive model.

**Outputs:** burden-band retention, expected/experienced gaps, shift-by-burden comparisons, missingness summary.  
**Verification:** hand-calculated monthly costs; round-trip and band boundaries; no attendance-based extrapolation.

## Investigation 3 Scheduling and flexibility

**Script:** analysis/03_scheduling.sql  
**Requirements:** INV-03

Baseline preference mismatch means PreferredShift is neither Any nor the initial effective ShiftCode. Compare advertised and assigned shift/weekend/holiday requirements. Report schedule consistency and transfer availability. For experienced schedules use the interval effective on day 14.

Request counts use request dates within the reporting cutoff and status as known then. A request resolved after AsOfDate is pending at that cutoff. Report approved, denied, and unresolved requests separately. Requests can be associated with dissatisfaction or opportunity to stay long enough to request, so do not compare “ever requested” groups as baseline risk.

**Outputs:** baseline schedule retention, commute-by-schedule strata, request demand and outcomes, schedule-history examples.  
**Verification:** adjacent schedule intervals, denied requests, approved transitions, and historical pending status.

## Investigation 4 Job experience and training

**Script:** analysis/04_job_experience.sql  
**Requirements:** INV-04

Use training recorded through day 7 for day-7-to-day-30 comparisons: sessions, distinct trainers, completion, and reported conflict. Use survey fit, confidence, consistency, and satisfaction through day 14 for day-14-to-day-90 comparisons. Summarize advertised and reported duties as contextual examples, not automatically scored truth.

Report response coverage and departures before each landmark. Multiple trainers alone do not prove inconsistent training; report that count alongside direct reported consistency/conflict.

**Outputs:** onboarding and survey score strata, early departures, coverage and unknowns.  
**Verification:** post-landmark observations cannot change earlier group membership; NULL conflict is not false.

## Investigation 5 Career mobility

**Script:** analysis/05_career_mobility.sql  
**Requirements:** INV-05

Report event counts by type, days from placement start to event, goal alignment, role level, and observed follow-up. Use ROW_NUMBER to select first qualifying advancement for time-to-first-event summaries; label median/average times as conditional on an observed event.

Use the day-180-to-day-270 landmark only for internal promotions compatible with continuous placement. Compare promoted and nonpromoted survivors within role/site strata. Separately report conversions and transfers, resulting placements where known, and explicit agency departure. Do not invent retention at the client after conversion.

**Outputs:** event summary, time to observed advancement, goal-alignment mix, landmark comparison, unknown outcomes.  
**Verification:** future goals/promotions cannot leak backward; positive conversions remain distinguishable from voluntary losses.

## Investigation 6 Combined retention patterns

**Script:** analysis/06_combined_patterns.sql  
**Requirements:** INV-06

Compare burden and overnight work, burden and schedule mismatch, early job experience and training, and career expectations/mobility within the appropriate observation windows. Use the common day-14 landmark for experienced commute/survey combinations; use the day-180 landmark for observed mobility combinations. Do not join these into a single inconsistent risk model.

Start with site, role level, and cohort-period strata. Show four-cell interaction tables where appropriate, sample counts, retained counts, and percentage-point differences. Identify unstable or sparse comparisons and cases where grouping changes an apparent overall association. Include supportive conditions and mixed findings.

**Outputs:** comparable segment tables and interpreted patterns; no causal ranking or predictive score.  
**Verification:** each group uses the same eligibility window and measurement timing, including an example confounded raw average.

## Investigation 7 Business impact and recommendations

**Script:** analysis/07_business_impact.sql  
**Requirements:** INV-07

Count replacement starts, unfilled ended vacancies where identifiable, repeated cohort starts, and recruiting and training costs. Distinguish all observed event flows from mature-cohort retention denominators.

Placement onboarding cost = its RecruitmentCostUSD plus its training-session costs. Summarize cost invested in voluntary/involuntary early departures as “modeled onboarding cost associated with early exits,” not a proven avoidable loss.

For realized replacement cost, attribute the linked successor's recruiting and training costs once to the replacement start. Never also add the departing worker's onboarding cost into the same replacement-cost total. Restrict “early-turnover replacement” to successors linked to qualifying early exits.

Hypothetical scenario: avoided eligible exits = eligible placements × assumed absolute percentage-point improvement / 100. Gross modeled savings = avoided exits × observed or explicitly assumed replacement cost per relevant case. Net scenario benefit = gross savings minus hypothetical intervention cost over a matching time period. If observed unit cost is unavailable, report unavailable or use a clearly labeled supplied assumption.

**Outputs:** hiring/cost reconciliation, high-burden segments, scenario table, findings-linked recommendations with KPIs.  
**Verification:** no duplicate cost attribution, consistent time basis, zero improvement yields zero gross savings, and negative net scenarios remain visible.

## Reporting reuse and delivery

Proposed shared objects are vw_PlacementDimensions, vw_PlacementOnboardingCost, and parameterized usp_RetentionSummary, usp_CommuteScheduleSummary, usp_ExperienceMobilitySummary, usp_ClientRoleExplorer, and usp_BusinessImpact. Names may be refined during implementation; definitions must not diverge from this contract. Investigation scripts explain and exercise the SQL, rather than hiding all work behind unexplained calls.

Record findings only after running validated queries. The findings report links each claim to script, parameters, dataset manifest, output, limitations, and recommended follow-up KPI. A weak or contradictory pattern is a valid result. No current document claims that any hypothesis has been confirmed.
