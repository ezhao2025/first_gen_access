
import pandas as pd
match = pd.read_csv("data/interim/trio_matches.csv")
auto = match[match.score >= 95]
print("auto matches:", len(auto))
print(auto.sample(20, random_state=99)
      [["recipient_name", "matched_name", "state", "city", "score"]].to_string(index=False))
