
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

Path("docs/img").mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 140, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})

df = pd.read_csv("data/processed/institutions.csv")
match = pd.read_csv("data/interim/trio_matches.csv")
df["has_trio"] = df.UNITID.isin(match[match.score >= 95].UNITID).astype(int)
df["gap"] = df.nonpell_rate - df.pell_rate

# 1. gap distribution
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.hist(df.gap, bins=60, color="#4a6fa5", edgecolor="white", linewidth=.3)
ax.axvline(0, color="#333", lw=1)
ax.axvline(df.gap.mean(), color="#c1442e", lw=1.5, ls="--",
           label=f"mean {df.gap.mean():.3f}")
ax.set_xlim(-0.35, 0.35)
ax.set_xlim(-0.35, 0.35)
ax.set_xlabel("Completion gap (non-Pell − Pell)")
ax.set_ylabel("Institutions")
ax.set_title("The Pell gap varies enormously across institutions")
ax.legend(frameon=False)
fig.tight_layout(); fig.savefig("docs/img/gap_dist.png"); plt.close(fig)

# 2. locale effect (odds ratios from the GLM)
labels = ["Suburb", "Town", "Rural"]
or_ = [1.002, 0.891, 0.923]
lo = [0.952, 0.850, 0.871]
hi = [1.057, 0.929, 0.980]
fig, ax = plt.subplots(figsize=(6.8, 3))
y = np.arange(len(labels))
ax.errorbar(or_, y, xerr=[np.array(or_)-np.array(lo), np.array(hi)-np.array(or_)],
            fmt="o", color="#4a6fa5", capsize=4)
ax.axvline(1, color="#c1442e", lw=1, ls="--")
ax.set_yticks(y); ax.set_yticklabels(labels)
ax.set_xlabel("Odds ratio vs. city institutions (95% CI)")
ax.set_title("Pell students complete at lower odds in towns and rural areas")
fig.tight_layout(); fig.savefig("docs/img/locale_or.png"); plt.close(fig)

# 3. TRIO coverage vs gap by locale
g = df.groupby("locale4").agg(trio_cov=("has_trio","mean"), gap=("gap","mean"))
names = {1:"City", 2:"Suburb", 3:"Town", 4:"Rural"}
fig, ax = plt.subplots(figsize=(5.2, 3.6))
ax.scatter(g.trio_cov*100, g.gap, s=90, color="#4a6fa5")
for i, r in g.iterrows():
    ax.annotate(names[i], (r.trio_cov*100, r.gap), xytext=(6, 4),
                textcoords="offset points")
ax.margins(x=0.18)
ax.margins(x=0.18)
ax.set_xlabel("Institutions with TRIO SSS (%)")
ax.set_ylabel("Mean Pell completion gap")
ax.set_title("Federal support coverage vs. the gap")
fig.tight_layout(); fig.savefig("docs/img/trio_coverage.png"); plt.close(fig)

print("wrote 3 charts to docs/img/")
