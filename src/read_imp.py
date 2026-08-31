
import pandas as pd

pd.set_option("display.max_rows", None, "display.width", 220, "display.max_colwidth", 90)
xl = pd.ExcelFile("data/raw/ipeds2024/om2024.xlsx")
print(xl.parse("Imputation values").to_string())
