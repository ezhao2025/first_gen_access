
import pandas as pd, glob

f = glob.glob("data/raw/trio/Assistance_*.csv")[0]
df = pd.read_csv(f, low_memory=False)
print("awards:", len(df))

trio = (df[["recipient_name", "recipient_state_code", "recipient_city_name",
            "recipient_uei"]]
        .dropna(subset=["recipient_name"])
        .drop_duplicates(subset=["recipient_name", "recipient_state_code"]))
print("unique institutions:", len(trio))
trio.to_csv("data/interim/trio_grantees.csv", index=False)
