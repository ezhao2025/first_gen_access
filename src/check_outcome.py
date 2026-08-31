
import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
df["pell_rate"] = df.pell_omawdn8 / df.pell_omachrt
print(df[["pell_rate", "nonpell_rate", "pell_omachrt"]].describe().round(3))
print("\ngap (nonpell - pell):")
print((df.nonpell_rate - df.pell_rate).describe().round(3))
print("\nflag values in raw OM:")
import sys; sys.path.insert(0, "src")
from load import load
om = load("om2024")
print(om[om.OMCHRT.isin([11,12])].XOMAWDN8.value_counts())
