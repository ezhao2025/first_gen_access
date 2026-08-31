
import sys; sys.path.insert(0, "src")
import pandas as pd
from load import load

om = load("om2024")
om = om[om.OMCHRT == 11][["UNITID", "OMACHRT", "OMCERT8", "OMASSC8", "OMBACH8", "OMAWDN8"]]
hd = load("hd2024")[["UNITID", "CONTROL", "ICLEVEL"]]
m = om.merge(hd, on="UNITID")
m["cert_share"] = m.OMCERT8 / m.OMAWDN8
m["bach_share"] = m.OMBACH8 / m.OMAWDN8
print(m.groupby("CONTROL")[["cert_share", "bach_share"]].mean().round(3))
print(m.groupby(["CONTROL", "ICLEVEL"])[["cert_share", "bach_share"]].mean().round(3))
print((m.OMAWDN8 == 0).sum(), "institutions with zero awards at 8yr")
