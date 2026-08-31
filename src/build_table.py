
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
# hd2024     -> CONTROL, ICLEVEL, LOCALE, STOBBR, INSTNM, HBCU
# ef2024d    -> retention rate, student-faculty ratio
# sfa2324    -> pct undergrads awarded Pell
# adm2024    -> admit rate (only ~1,956 institutions — decide how to handle)
#
# Use load(), left-merge on UNITID, and log() after every merge.

wide.to_csv("data/processed/institutions.csv", index=False)
log("FINAL", wide)
