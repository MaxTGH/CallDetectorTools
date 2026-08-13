'''
Author: MN
Date: 8/13/26

Description:
    Fills missing source file values and removes HAT02A detections after the cutoff.
'''

import pandas as pd

input_file = r"F:\detections\Relabeledv2\combined_detections_verified_MN_reviewed.txt"
output_file = r"F:\detections\Relabeledv2\combined_detections_verified_MN_reviewed_filtered.txt"

# Read the tab-delimited file
df = pd.read_csv(input_file, sep="\t")

# Fill missing source_txt_file values
missing_mask = (
    df["source_txt_file"].isna() |
    (df["source_txt_file"].astype(str).str.strip() == "") |
    (df["source_txt_file"].astype(str).str.lower().isin(["nan", "none"]))
)

print(f"Updating {missing_mask.sum()} rows.")

df.loc[missing_mask, "source_txt_file"] = "HAT02A_allLF_cleaned_CMSS_verified.txt"

# Convert start_time to datetime
df["start_time"] = pd.to_datetime(df["start_time"])

cutoff = pd.Timestamp("2013-01-01 23:22:00.000")

# Remove HAT02A detections after the cutoff
remove_mask = (
    (df["source_txt_file"] == "HAT02A_allLF_cleaned_CMSS_verified.txt") &
    (df["start_time"] > cutoff)
)

print(f"Removing {remove_mask.sum()} rows.")

# Keep all other rows
df_filtered = df.loc[~remove_mask]

# Save to a new file
df_filtered.to_csv(output_file, sep="\t", index=False)

print(f"Original rows: {len(df)}")
print(f"Remaining rows: {len(df_filtered)}")
print(f"Saved filtered file to:\n{output_file}")

print("\nLabel counts:")
label_counts = df_filtered["label"].value_counts().sort_index()
print(label_counts)