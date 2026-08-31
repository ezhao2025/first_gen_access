
import pandas as pd
df = pd.read_csv("data/processed/institutions.csv")
df["gap"] = df.nonpell_rate - df.pell_rate
df["locale4"] = df.LOCALE // 10

print("by CONTROL (1=public 2=private-np 3=for-profit):")
print(df.groupby("CONTROL").gap.agg(["mean", "median", "count"]).round(3))
print("\nby ICLEVEL (1=4yr 2=2yr):")
print(df.groupby("ICLEVEL").gap.agg(["mean", "median", "count"]).round(3))
print("\nby locale (1=city 2=suburb 3=town 4=rural):")
print(df.groupby("locale4").gap.agg(["mean", "median", "count"]).round(3))
print("\nHBCU (1=yes 2=no):")
print(df.groupby("HBCU").gap.agg(["mean", "median", "count"]).round(3))
