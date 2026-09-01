
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("data/processed/institutions.csv")
print("start:", len(df))

# --- decisions you should be able to defend --------------------------------
df = df.dropna(subset=["RET_PCF", "cert_share", "nonpell_rate"])
print("after dropna:", len(df))

FORMULA = ("pell_omawdn8 + pell_fail ~ nonpell_rate + cert_share + RET_PCF "
           "+ C(CONTROL) + C(ICLEVEL) + C(locale4) + is_open_admission")

m = smf.glm(FORMULA, data=df, family=sm.families.Binomial()).fit(cov_type="HC1")
print(m.summary())

# --- overdispersion --------------------------------------------------------
pearson_chi2 = m.pearson_chi2
disp = pearson_chi2 / m.df_resid
print(f"\noverdispersion (Pearson chi2/df): {disp:.2f}")
print("  >>1 means SEs from a naive Binomial fit would be too small;")
print("  HC1 robust SEs are already in use above.")

# --- odds ratios -----------------------------------------------------------
odds = pd.DataFrame({
    "OR": np.exp(m.params),
    "lo": np.exp(m.conf_int()[0]),
    "hi": np.exp(m.conf_int()[1]),
})
print("\nodds ratios:")
print(odds.round(3))
# --- refit with dispersion-scaled SEs --------------------------------------
m2 = smf.glm(FORMULA, data=df, family=sm.families.Binomial()).fit()
disp = m2.pearson_chi2 / m2.df_resid
se_scaled = m2.bse * np.sqrt(disp)
z = m2.params / se_scaled
from scipy import stats
p_scaled = 2 * (1 - stats.norm.cdf(np.abs(z)))
print(pd.DataFrame({"coef": m2.params.round(3),
                    "p_HC1": m.pvalues.round(3),
                    "p_qb": p_scaled.round(3)}))

# --- VIF -------------------------------------------------------------------
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrix
X = dmatrix(FORMULA.split("~")[1], data=df, return_type="dataframe")
vif = pd.DataFrame({
    "var": X.columns,
    "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
})
print("\nVIF:")
print(vif.round(2).to_string(index=False))

# --- holdout ---------------------------------------------------------------
rng = np.random.default_rng(42)
mask = rng.random(len(df)) < 0.8
train, test = df[mask], df[~mask]
mh = smf.glm(FORMULA, data=train, family=sm.families.Binomial()).fit(scale="X2")
pred = mh.predict(test)
actual = test.pell_omawdn8 / test.pell_omachrt
print(f"\nholdout n={len(test)}")
print(f"  MAE:  {np.abs(pred - actual).mean():.4f}")
print(f"  corr: {np.corrcoef(pred, actual)[0,1]:.3f}")