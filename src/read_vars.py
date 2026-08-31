
import pandas as pd

pd.set_option("display.max_rows", None, "display.width", 220, "display.max_colwidth", 90)
xl = pd.ExcelFile("data/raw/ipeds2024/om2024.xlsx")
vl = xl.parse("Varlist")
print("COLUMNS:", list(vl.columns), "\n")
print(vl.to_string())
