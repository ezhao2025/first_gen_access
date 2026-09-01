
# Phase 3 results — FTFT Pell completion, 2016-17 cohort, 8-year status point

n = 2,517 institutions (after dropping missing retention)
Binomial GLM, logit link, on counts (awards / adjusted cohort)

Overdispersion: Pearson chi2/df = 12.15 — severe. Reported p-values are the
more conservative of HC1-robust and quasi-binomial for each coefficient.

Holdout (20%, n=512): MAE 0.067, corr 0.864
(Pseudo-R2 saturates at 1.000 on grouped binomial data — not reported.)

## Robust findings
- nonpell_rate OR 15.6 — institutional performance dominates. The Pell gap
  is mostly NOT explained by sector/level/locale; it tracks how well the
  institution serves everyone.
- Town locale OR 0.889 vs city — Pell students at town institutions complete
  at lower odds even holding institutional performance constant.
- Rural locale OR 0.924 vs city — same direction, smaller.
- For-profit OR 1.368 — survives cert_share control; award mix does not
  fully explain it.
- RET_PCF OR 1.015 per point of retention.

## Fragile
- cert_share OR 1.26 — significant under HC1 (p=.014), unstable across
  corrections. Report with caveat.
- is_open_admission — null under HC1 (p=.152). Report as null.

## Null
- Private nonprofit vs public; 2yr vs 4yr; suburb vs city.

## Diagnostics
VIF max 3.37 (ICLEVEL) — no collinearity problem.

## Phase 3b — clustering (null result)
K-means on structural features only (control, level, locale, size,
retention, student-faculty ratio); outcome variables excluded to avoid
circularity.

Silhouette across k=2..20: rises monotonically from 0.200 to 0.415 with no
elbow, never exceeding 0.5.

=> No natural cluster structure. Institutions vary continuously in
effectiveness rather than falling into discrete archetypes. Consistent
with the GLM result that nonpell_rate (OR 15.6) dominates every
categorical predictor: the meaningful variation is a continuum, not
a typology.

## Phase 4 — TRIO SSS join
Source: USASpending, CFDA 84.042, FY2016-2020 activity. 2,777 awards,
966 unique grantees. Joined to IPEDS by state+city block, then fuzzy
name match (token_sort_ratio). 917/966 blocked on state+city.
Auto-accept >=95: 623 matches. 622 institutions in modeling sample.

Descriptive: TRIO institutions have LOWER completion for both groups
(Pell .425 vs .499; non-Pell .509 vs .564) and a WIDER gap (.083 vs .066).
0% of for-profits hold SSS grants; 33.5% of publics do.

Conditional (GLM): has_trio OR 0.930, significant under HC1 and quasi-binomial.

INTERPRETATION: This is selection, not program effect. TRIO is competitively
awarded to institutions serving students with barriers the covariates do not
capture. The negative coefficient marks unmeasured need. No causal claim is
possible from this design; identifying a program effect would require matching
on pre-award characteristics or a discontinuity around funding thresholds.

Main findings unchanged by adding has_trio — specification is stable.
