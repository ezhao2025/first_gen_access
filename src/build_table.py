
import sys
sys.path.insert(0, "src")
import pandas as pd
from load import load

KEEP_FLAGS = {"R", "C"}

def log(label, df):
    print(f"{label:32s} {len(df):>6,} rows")

# ---- outcome: OM, long -> wide -------------------------------------------
om = load("om2024")
log("om2024 raw", om)

om = om[om.OMCHRT.isin([11, 12])]
log("FTFT Pell + non-Pell", om)

om = om[om.XOMACHRT.isin(KEEP_FLAGS) & om.XOMAWDN8.isin(KEEP_FLAGS)]
log("after imputation filter", om)

wide = om.pivot(index="UNITID", columns="OMCHRT", values=["OMACHRT", "OMAWDN8"])
wide.columns = [f"{'pell' if c == 11 else 'nonpell'}_{v.lower()}" for v, c in wide.columns]
wide = wide.reset_index()
log("pivoted to one row/inst", wide)

wide = wide.dropna(subset=["pell_omachrt", "pell_omawdn8",
                           "nonpell_omachrt", "nonpell_omawdn8"])
log("both subcohorts present", wide)

wide = wide[(wide.pell_omachrt >= 30) & (wide.nonpell_omachrt >= 30)]
log("both cohorts >= 30", wide)

# failures column for the binomial GLM
wide["pell_fail"] = wide.pell_omachrt - wide.pell_omawdn8
wide["nonpell_rate"] = wide.nonpell_omawdn8 / wide.nonpell_omachrt
wide["pell_rate"] = wide.pell_omawdn8 / wide.pell_omachrt


# ---- YOUR PART: merge features -------------------------------------------
# ---- features -------------------------------------------------------------
hd = load("hd2024")[["UNITID", "INSTNM", "STABBR", "SECTOR", "ICLEVEL", "CONTROL",
                     "HBCU", "TRIBAL", "LOCALE", "INSTSIZE", "C21BASIC", "WEBADDR"]]
wide = wide.merge(hd, on="UNITID", how="left")
log("+ hd2024", wide)
print("   missing CONTROL:", wide.CONTROL.isna().sum())

ef = load("ef2024d")[["UNITID", "RET_PCF", "STUFACR"]]
wide = wide.merge(ef, on="UNITID", how="left")
log("+ ef2024d", wide)
print("   missing retention:", wide.RET_PCF.isna().sum())

adm = load("adm2024")[["UNITID", "APPLCN", "ADMSSN"]]
adm["admit_rate"] = adm.ADMSSN / adm.APPLCN
wide = wide.merge(adm[["UNITID", "admit_rate"]], on="UNITID", how="left")
log("+ adm2024", wide)
print("   missing admit rate:", wide.admit_rate.isna().sum())

wide.to_csv("data/processed/institutions.csv", index=False)
log("FINAL", wide)
