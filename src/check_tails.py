
import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
df["pell_rate"] = df.pell_omawdn8 / df.pell_omachrt
df["gap"] = df.nonpell_rate - df.pell_rate
print(df.nonpell_omachrt.describe().round(1))
print("\nnonpell cohort < 30:", (df.nonpell_omachrt < 30).sum())
print("\nextreme gaps (|gap| > 0.4) — nonpell cohort sizes:")
print(df.loc[df.gap.abs() > 0.4, "nonpell_omachrt"].describe().round(1))
