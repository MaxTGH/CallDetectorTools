'''
Author: MN
Date: 8/13/26

Description:
    Keeps only detections from the NFC_A_03 deployment.
'''

import pandas as pd


# Input/output files
input_file = r"F:\Model_1\detections\raw_detections.txt"
output_file = r"F:\Model_1\detections\raw_detections_NFC_A_03.txt"

# Read tab-delimited file
df = pd.read_csv(input_file, sep="\t")

print(f"Total rows before filtering: {len(df):,}")

# Keep only rows where wav_file_path contains NFC_A_03
df = df[df["wav_file_path"].str.contains(
    r"F:/Model_1/InferenceXwavs\\NFC_A_03",
    regex=True,
    na=False
)]

print(f"Total rows after filtering: {len(df):,}")

# Save filtered file
df.to_csv(output_file, sep="\t", index=False)

print(f"Saved filtered file to: {output_file}")