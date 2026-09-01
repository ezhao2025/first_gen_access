
import sys; sys.path.insert(0, "src")
from load import load

NAMES = ["Rio Salado", "Wayne Community College", "Columbia Central"]
hd = load("hd2024")[["UNITID", "INSTNM"]]
om = load("om2024")

for n in NAMES:
    ids = hd[hd.INSTNM.str.contains(n, case=False, na=False)]
    for _, h in ids.iterrows():
        sub = om[(om.UNITID == h.UNITID) & (om.OMCHRT.isin([10, 11, 12]))]
        print(f"\n{h.INSTNM} ({h.UNITID})")
        print(sub[["OMCHRT", "OMRCHRT", "OMEXCLS", "OMACHRT",
                   "OMCERT8", "OMASSC8", "OMBACH8", "OMAWDN8"]].to_string(index=False))
