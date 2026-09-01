
import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
print(df.cert_mix_diff.describe().round(3))
print("\nmissing:", df.cert_mix_diff.isna().sum())
print("\n|diff| > 0.5:", (df.cert_mix_diff.abs() > 0.5).sum(), "institutions")
