
import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("data/processed/institutions.csv")
df = df.dropna(subset=["RET_PCF", "STUFACR", "nonpell_rate"])
print("n =", len(df))

# structural features only — the outcome stays out
X = pd.get_dummies(df[["CONTROL", "ICLEVEL", "locale4", "INSTSIZE",
                       "RET_PCF", "STUFACR"]],
                   columns=["CONTROL", "ICLEVEL", "locale4", "INSTSIZE"])
Xs = StandardScaler().fit_transform(X)

print("\nk  silhouette")
for k in range(2, 21):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
    print(f"{k:2d}  {silhouette_score(Xs, km.labels_):.3f}")
