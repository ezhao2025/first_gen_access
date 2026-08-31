
# OM2024 variable notes
Source: data/raw/ipeds2024/om2024.xlsx
Cohort: entered 2016-17; 8-year status point = Aug 31, 2024
Format: LONG — up to 15 rows per institution (OMCHRT), not 8

## OMCHRT codes  [sheet: Frequencies]
Two digits: cohort | Pell status (0=total, 1=Pell, 2=non-Pell)
50/51/52  all entering
10/11/12  first-time full-time      <- MODELING THIS
20/21/22  first-time part-time
30/31/32  non-first-time full-time  <- robustness check
40/41/42  non-first-time part-time

## Outcome variables  [sheet: Varlist]
| variable | meaning |
|---|---|
| OMACHRT  | adjusted cohort (denominator) |
| OMAWDN8  | awards at 8 years (numerator) |
| OMRCHRT  | raw cohort before exclusions — NOT used |
| OMAWDP8  | percent — NOT used, need counts for binomial GLM |

## Imputation flags  [sheet: Imputation values]
XOMACHRT, XOMAWDN8 — values TBD, see src/read_imp.py output

## Decision
Cohort 11/12 (FTFT Pell / non-Pell). Standard comparison group, largest N.
Limitation: excludes part-time and transfer students, who skew lower-income,
so this likely understates the overall Pell gap.

## Imputation flag values  [sheet: Imputation values]
R = Reported                          <- KEEP
C = Analyst corrected reported value  <- KEEP
A = Not applicable
B = Institution left item blank
D = Do not know
G = Generated from other data values
H = Value not derived - not usable
J = Logical imputation
K = Ratio adjustment
L = Imputed, Group Median
N = Imputed, Nearest Neighbor
P = Imputed, Carry Forward
Z = Implied zero

Filter: keep XOMACHRT and XOMAWDN8 in {R, C}. Report drop count.

## Award mix finding (important)
OMAWDN8 counts any award: certificate, associate's, or bachelor's.
Award mix differs sharply by sector:
  public 4yr:            3.8% cert / 70.3% bach
  private nonprofit 4yr: 2.4% cert / 89.0% bach
  for-profit 2yr:       72.0% cert /  0.4% bach

=> The narrow for-profit "Pell gap" (0.007) is an artifact of award mix,
   not evidence of equitable outcomes. Certificates are short and
   near-universally completed.

Decision: report cert_share alongside the gap, AND include it as a
covariate in the GLM. Do not restrict to 4yr — that would drop the
community colleges where most Pell students enroll.
