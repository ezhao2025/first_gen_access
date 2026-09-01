
import pandas as pd, glob
f = glob.glob("data/raw/trio/Assistance_*.csv")
print("file:", f[0])
df = pd.read_csv(f[0], low_memory=False)
print("shape:", df.shape)
print("\ncolumns:")
for c in df.columns:
    print("  ", c)
