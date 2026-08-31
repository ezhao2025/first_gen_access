
import pandas as pd, sys

pd.set_option("display.max_rows", None, "display.width", 220, "display.max_colwidth", 95)
name = sys.argv[1]
xl = pd.ExcelFile(f"data/raw/ipeds2024/{name}.xlsx")
print("SHEETS:", xl.sheet_names, "\n")
print(xl.parse("Varlist")[["varName", "varTitle"]].to_string())
