'''
Author: MN
Date: 8/13/26

Description:
    Removes 40Hz calls and adds 1 second to Bp_20Hz call end times.
'''


import pandas as pd

# Input and output files
input_file = r"F:\detections\Raw\HAT02A_allLF_cleaned_CMSS_verified.txt"
output_file = r"F:\detections\Raw\HAT02A_allLF_cleaned_CMSS_verifiedv2.txt"

# Read tab-delimited file
df = pd.read_csv(input_file, sep="\t")

# Remove rows where label contains "40Hz"
df = df[~df["label"].astype(str).str.contains("40Hz", na=False)]

# Find remaining rows where label contains "Bp_20Hz"
mask = df["label"].astype(str).str.contains("Bp_20Hz", na=False)

# Convert end_time to datetime
df["end_time"] = pd.to_datetime(df["end_time"])

# Add 1 second to end_time
df.loc[mask, "end_time"] += pd.Timedelta(seconds=1)

# Convert back to original format
df["end_time"] = df["end_time"].dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]

# Save as tab-delimited
df.to_csv(output_file, sep="\t", index=False)

print(f"Removed {(~df['label'].astype(str).str.contains('40Hz', na=False)).sum()} 40Hz calls.")
print(f"Updated {mask.sum()} Bp_20Hz calls.")
print(f"Saved to:\n{output_file}")