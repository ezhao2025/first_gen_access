
import pandas as pd

pd.set_option("display.max_rows", None, "display.width", 220, "display.max_colwidth", 70)
xl = pd.ExcelFile("data/raw/ipeds2024/om2024.xlsx")

freq = xl.parse("Frequencies")
print("COLUMNS:", list(freq.columns), "\n")
print(freq[freq.iloc[:, 0].astype(str).str.upper().str.strip() == "OMCHRT"].to_string())
