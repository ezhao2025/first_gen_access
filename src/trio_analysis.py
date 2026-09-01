
import pandas as pd

inst = pd.read_csv("data/processed/institutions.csv")
match = pd.read_csv("data/interim/trio_matches.csv")

matched = set(match[match.score >= 95].UNITID)
inst["has_trio"] = inst.UNITID.isin(matched).astype(int)
inst["gap"] = inst.nonpell_rate - inst.pell_rate

print("institutions with TRIO SSS:", inst.has_trio.sum(), "of", len(inst))

print("\ncompletion rates:")
print(inst.groupby("has_trio")[["pell_rate", "nonpell_rate", "gap"]].mean().round(3))

print("\nTRIO rate by sector (1=public 2=private-np 3=for-profit):")
print(inst.groupby("CONTROL").has_trio.mean().round(3))

print("\nTRIO rate by level (1=4yr 2=2yr):")
print(inst.groupby("ICLEVEL").has_trio.mean().round(3))

import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from scipy import stats

df = inst.dropna(subset=["RET_PCF", "cert_share", "nonpell_rate", "locale4"]).copy()
df["pell_fail"] = df.pell_omachrt - df.pell_omawdn8

F = ("pell_omawdn8 + pell_fail ~ nonpell_rate + cert_share + RET_PCF "
     "+ C(CONTROL) + C(ICLEVEL) + C(locale4) + is_open_admission + has_trio")

m = smf.glm(F, data=df, family=sm.families.Binomial()).fit(cov_type="HC1")
m2 = smf.glm(F, data=df, family=sm.families.Binomial()).fit()
disp = m2.pearson_chi2 / m2.df_resid
p_qb = 2 * (1 - stats.norm.cdf(np.abs(m2.params / (m2.bse * np.sqrt(disp)))))

print("\nGLM with has_trio:")
print(pd.DataFrame({"coef": m.params.round(3), "OR": np.exp(m.params).round(3),
                    "p_HC1": m.pvalues.round(3), "p_qb": p_qb.round(3)}))
