'''
Author: MN
Date: 8/13/26

Description:
    Removes all annotations with MFA labels from the file.
'''

import pandas as pd

file_path = r"F:\Model_3\Test\new_examples.txt"

# Read file
df = pd.read_csv(file_path, sep="\t")

# Look at all labels first
print("Labels before filtering:")
print(df["label"].value_counts(dropna=False))

# Find MFA rows
mfa_mask = df["label"].astype(str).str.contains(
    "MFA",
    case=False,
    na=False
)

print("\nNumber of MFA rows:", mfa_mask.sum())

print("\nMFA labels being removed:")
print(df.loc[mfa_mask, "label"].value_counts())

# Remove MFA rows
df = df.loc[~mfa_mask].copy()

print("\nLabels after filtering:")
print(df["label"].value_counts(dropna=False))

# Save back to the same file
df.to_csv(
    file_path,
    sep="\t",
    index=False
)

print(f"\nSaved cleaned file to:\n{file_path}")