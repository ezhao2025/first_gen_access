
import pandas as pd

FILES = ["hd2024", "om2024", "gr2024", "sfa2324", "adm2024", "ef2024d"]

for f in FILES:
    df = pd.read_csv(f"data/raw/ipeds2024/{f}.csv", encoding="latin-1", low_memory=False)
    print(f"\n{f}: {len(df):,} rows, {len(df.columns)} cols")
    print("  first 5 cols:", list(df.columns[:5]))
