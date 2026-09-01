
import pandas as pd, re, sys
sys.path.insert(0, "src")
from rapidfuzz import process, fuzz
from load import load

inst = pd.read_csv("data/processed/institutions.csv")
hd = load("hd2024")[["UNITID", "CITY"]]
inst = inst.merge(hd, on="UNITID", how="left")
trio = pd.read_csv("data/interim/trio_grantees.csv")

def norm(s):
    s = str(s).upper()
    s = re.sub(r"\b(THE|AT|OF|AND|INC)\b", " ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

inst["key"] = inst.INSTNM.map(norm)
inst["city_k"] = inst.CITY.map(norm)
trio["key"] = trio.recipient_name.map(norm)
trio["city_k"] = trio.recipient_city_name.map(norm)

rows = []
for _, r in trio.iterrows():
    pool = inst[(inst.STABBR == r.recipient_state_code) & (inst.city_k == r.city_k)]
    blocked_on = "state+city"
    if pool.empty:                        # fall back to state only
        pool = inst[inst.STABBR == r.recipient_state_code]
        blocked_on = "state"
    if pool.empty:
        continue
    choices = dict(zip(pool.UNITID, pool.key))
    m = process.extractOne(r.key, choices, scorer=fuzz.token_sort_ratio)
    if m:
        rows.append({"recipient_name": r.recipient_name,
                     "state": r.recipient_state_code, "city": r.recipient_city_name,
                     "UNITID": m[2], "matched_name": m[0],
                     "score": m[1], "blocked_on": blocked_on})

match = pd.DataFrame(rows)
print(match.blocked_on.value_counts())
for lo, hi, lbl in [(95, 101, "auto  >=95"), (88, 95, "review 88-95"), (0, 88, "reject <88")]:
    print(f"{lbl}: {((match.score >= lo) & (match.score < hi)).sum()}")

print("\ndupes (same UNITID matched twice):",
      match[match.score >= 88].UNITID.duplicated().sum())

match.sort_values("score").to_csv("data/interim/trio_matches.csv", index=False)
print("\nsample from auto band:")
print(match[match.score >= 95].sample(15, random_state=1)
      [["recipient_name", "matched_name", "score", "blocked_on"]].to_string(index=False))

print("\nreject band sample (are these real misses?):")
print(match[match.score < 88].sample(15, random_state=2)
      [["recipient_name", "matched_name", "score", "blocked_on"]].to_string(index=False))
