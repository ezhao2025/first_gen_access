

import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
for var in ["CONTROL", "ICLEVEL"]:
    print(f"\nby {var}:")
    print(df.groupby(var)[["pell_rate", "nonpell_rate"]].mean().round(3))
