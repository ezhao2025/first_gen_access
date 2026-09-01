# Where does the Pell completion gap live?

An institution-level analysis of completion disparities between Pell Grant recipients and non-recipients across 2,517 U.S. postsecondary institutions.

## Question

Pell recipients complete degrees at lower rates than their peers. Is that gap explained by *what kind of institution* a student attends — sector, level, urbanicity, size — or by something else?

## Data

IPEDS Outcome Measures (OM2024), 2024-25 collection. The cohort entered in **2016-17**; the eight-year status point is **August 31, 2024**.

The outcome is the first-time full-time subcohort (`OMCHRT` 11 = Pell, 12 = non-Pell), modeled as awards (`OMAWDN8`) out of adjusted cohort (`OMACHRT`). Institutional characteristics come from HD2024, retention and student-faculty ratio from EF2024D, admissions from ADM2024.

Filters: both subcohorts present, both cohorts ≥ 30 students, outcome values reported rather than imputed (`XOMACHRT` and `XOMAWDN8` in {R, C}). 47,029 raw rows → 2,699 institutions → 2,517 after dropping missing retention.

**IPEDS has no first-generation variable.** Pell receipt is used throughout as a socioeconomic proxy. This is a real limitation, not a synonym.

## Method

Binomial GLM with logit link, fit on counts rather than precomputed rates so institutions are weighted by cohort size. Non-Pell completion rate enters as a covariate, which turns every other coefficient into a *conditional* effect: not "does this institution do well" but "does it do well for Pell students given how well it does for everyone."

Overdispersion is severe (Pearson χ²/df = 12.15), so reported p-values are the more conservative of HC1-robust and quasi-binomial for each coefficient. VIF max 3.37 — no collinearity problem.

## Findings

**1. Institutional performance dominates everything else.** Non-Pell completion rate has an odds ratio of 15.6 (CI 12.0–20.2). Conditional on how well an institution serves its non-Pell students, sector and level explain almost nothing. The gap is less about *what kind* of school a student attends than about *how good* it is.

**2. Town and rural institutions carry a persistent shortfall.** Relative to city institutions, Pell students at town institutions complete at OR 0.889 (p < .001) and at rural institutions at OR 0.924 (p = .008) — after controlling for institutional performance. Suburban institutions are indistinguishable from urban ones. Geography matters in a way that survives the dominant covariate.

**3. There are no institutional archetypes.** K-means on structural features gives silhouette scores rising monotonically from 0.200 (k=2) to 0.415 (k=20) with no elbow and no value above 0.5. Institutions vary along a continuum of effectiveness rather than falling into discrete types — consistent with finding 1.

**Reported with caveats:** for-profit institutions show OR 1.368, surviving the award-mix control. Certificate share (OR 1.26) is significant under HC1 but unstable across corrections. Open-admission status is null (p = .152), as are private-nonprofit vs. public and two-year vs. four-year.

## A diagnostic that changed the answer

Descriptively, for-profits appeared to have almost no Pell gap (0.007 vs. 0.070 at publics). Checking award composition showed why the naive reading fails: at for-profit two-years, 72% of awards are certificates and 0.4% are bachelor's degrees, against 2.4% and 89% at private nonprofit four-years. `OMAWDN8` counts any award, so "completion" means different things at different institutions.

Certificate share was added as a covariate and is reported alongside the gap throughout. Without this check, the project would have reported that for-profits serve Pell students equitably — which the data does not support.

## Performance

80/20 holdout, n = 512 institutions: **MAE 0.067, correlation 0.864**.

Pseudo-R² saturates at 1.000 on grouped binomial data with large denominators and is not reported.

## Limitations

- Pell receipt is a proxy for socioeconomic status, not a first-generation measure.
- The first-time full-time cohort excludes part-time and transfer students, who skew lower-income. The gap reported here likely understates the overall disparity.
- Institutions with either subcohort under 30 were dropped. These skew toward small, specialized, and high-Pell institutions — some of the places where the equity question is most live.
- Admissions data is missing for 47% of institutions, almost entirely open-admission ones. Admit rate is therefore excluded from the model in favor of a binary open-admission indicator.
- Institution-level associations say nothing about individual students.

## Reproducing

```
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt
python src/build_table.py    # 47,029 rows -> 2,699 institutions
python src/model.py          # GLM, diagnostics, holdout
python src/cluster.py        # silhouette sweep
```

IPEDS raw files are not committed. Download HD2024, OM2024, GR2024, SFA2324, ADM2024, EF2024D and the finance files from the NCES Complete Data Files tool and place them in `data/raw/ipeds2024/`. Variable definitions and the imputation-flag codebook are in `notes/variables.md`.
