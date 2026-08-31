
import pandas as pd

RAW = "data/raw/ipeds2024"

def load(name):
    """Read an IPEDS CSV, handling BOM and non-UTF8 bytes."""
    try:
        df = pd.read_csv(f"{RAW}/{name}.csv", encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(f"{RAW}/{name}.csv", encoding="latin-1", low_memory=False)
    df.columns = df.columns.str.strip().str.upper()
    return df
