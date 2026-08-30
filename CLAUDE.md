
Project: institution-level Pell completion gap analysis + resource coverage audit.

Unit of analysis: institution (UNITID). Never student-level; we have no student data.

Data facts to respect:
- IPEDS has NO first-generation variable. Pell status is the socioeconomic proxy.
- First-gen share comes only from College Scorecard, merged on UNITID.
- The outcome is a proportion (completers / cohort), not a binary. Use a binomial
  GLM on counts. Do not use LogisticRegression on precomputed rates.

Rules:
- Never invent an IPEDS variable name. Read the dictionary xlsx shipped inside the
  zip and cite the sheet and row you got it from.
- Every merge must print row counts before and after. Unexpected drops are bugs.
- No model output is reported without a holdout number next to it.
- Raw files in data/raw/ are never edited or overwritten.

Environment: uv, Python 3.12. Use `uv pip install`, never bare pip — system pip is
broken on this machine (platform.mac_ver() returns empty on macOS 26).
