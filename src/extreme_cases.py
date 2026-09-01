
import pandas as pd

df = pd.read_csv("data/processed/institutions.csv")
match = pd.read_csv("data/interim/trio_matches.csv")
df["has_trio"] = df.UNITID.isin(match[match.score >= 95].UNITID).astype(int)
df["gap"] = df.nonpell_rate - df.pell_rate

CTRL = {1: "public", 2: "private nonprofit", 3: "for-profit"}
LVL  = {1: "4-year", 2: "2-year"}
LOC  = {1: "city", 2: "suburb", 3: "town", 4: "rural"}

cols = ["INSTNM", "STABBR", "CONTROL", "ICLEVEL", "locale4",
        "pell_rate", "nonpell_rate", "gap", "pell_omachrt", "has_trio"]

def show(title, sub):
    print(f"\n{title}")
    for _, r in sub.iterrows():
        print(f"  {r.INSTNM} ({r.STABBR}) — {CTRL.get(r.CONTROL,'?')} "
              f"{LVL.get(r.ICLEVEL,'?')}, {LOC.get(r.locale4,'?')}")
        print(f"      Pell {r.pell_rate:.1%} vs non-Pell {r.nonpell_rate:.1%} "
              f"= {r.gap:+.1%} gap | cohort {int(r.pell_omachrt)} | "
              f"TRIO {'yes' if r.has_trio else 'no'}")

# only institutions with enough students that the rate means something
big = df[(df.pell_omachrt >= 100) & (df.nonpell_omachrt >= 100)]
big = big[(big.nonpell_omachrt / (big.pell_omachrt + big.nonpell_omachrt)).between(0.2, 0.8)]
print(f"institutions with both cohorts >= 100: {len(big)}")

show("WIDEST GAPS", big.nlargest(5, "gap")[cols])
show("PELL STUDENTS OUTPERFORM MOST", big.nsmallest(5, "gap")[cols])
show("WIDEST GAPS AMONG TOWN INSTITUTIONS",
     big[big.locale4 == 3].nlargest(4, "gap")[cols])
