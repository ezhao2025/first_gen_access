
import pandas as pd
match = pd.read_csv("data/interim/trio_matches.csv")
rej = match[match.score < 88]
print("rejects:", len(rej))
print(rej.sample(20, random_state=7)
      [["recipient_name", "matched_name", "score", "blocked_on"]].to_string(index=False))
