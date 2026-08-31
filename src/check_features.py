
import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
print(df[["CONTROL", "ICLEVEL", "HBCU", "LOCALE"]].apply(pd.Series.value_counts).head(12))
print()
print(df[["RET_PCF", "STUFACR", "admit_rate", "pell_rate", "nonpell_rate"]].describe().round(2))
