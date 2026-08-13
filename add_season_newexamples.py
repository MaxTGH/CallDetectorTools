'''
Author: MN
Date: 8/13/26

Description:
    Adds a season column based on the date in each spectrogram filename for make_new_examples.
'''

import os
import re
import pandas as pd

# Input and output files
input_file = r"F:\Model_3\annotations\new_examples_with_deployment_id.txt"
output_file = r"F:\Model_3\annotations\new_examples_deployment_season.txt"

def get_season(month):
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"

def extract_date(filepath):
    # Handle mixed path separators
    filename = os.path.basename(str(filepath).replace("\\", "/"))

    match = re.search(r'(\d{8})T', filename)
    if match:
        return pd.to_datetime(match.group(1), format="%Y%m%d")

    return pd.NaT

print(f"Processing {os.path.basename(input_file)}...")

df = pd.read_csv(input_file, sep="\t", low_memory=False)

if "spectrogram_path" not in df.columns:
    raise ValueError("No 'spectrogram_path' column found.")

# Extract date and season
df["date"] = df["spectrogram_path"].apply(extract_date)
df["season"] = df["date"].dt.month.apply(
    lambda m: get_season(m) if pd.notna(m) else None
)

# Remove temporary date column
df.drop(columns=["date"], inplace=True)

# Save
df.to_csv(output_file, sep="\t", index=False)

print(f"Finished. Saved to:\n{output_file}")

print("\nSeason counts:")
print(df["season"].value_counts(dropna=False).sort_index())