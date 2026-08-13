'''
Author: MN
Date: 8/13/26

Description:
    Filters detections to a specified time window and adds the source file.
'''

import pandas as pd

file_path = r"F:\Model_3\Test\NFC_A_03_180100_145800_verified.txt"

# Read tab-delimited file
df = pd.read_csv(file_path, sep="\t")

# Convert start_time to datetime
df["start_time"] = pd.to_datetime(
    df["start_time"],
    format="%Y-%m-%d %H:%M:%S.%f"
)

# Define time window
start_time = pd.Timestamp("2018-04-09 18:01:00")
end_time   = pd.Timestamp("2018-04-10 14:58:00")

# Filter
df_filtered = df.loc[
    df["start_time"].between(start_time, end_time)
].copy()

# Add source file column
df_filtered["source_txt_file"] = "NFC_A_03_180000_145959_verified.txt"

# Check results
print(f"Original rows: {len(df):,}")
print(f"Filtered rows: {len(df_filtered):,}")

print("\nFiltered time range:")
print(df_filtered["start_time"].min())
print(df_filtered["start_time"].max())

# Save
output_file = r"F:\Model_3\Test\NFC_A_03_180100_145800_verified.txt"

df_filtered.to_csv(
    output_file,
    sep="\t",
    index=False
)

print(f"\nSaved to:\n{output_file}")