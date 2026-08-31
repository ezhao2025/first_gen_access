
import sys; sys.path.insert(0, "src")
from load import load
df = load(sys.argv[1])
print(f"{sys.argv[1]}: {len(df.columns)} columns\n")
print(list(df.columns))
