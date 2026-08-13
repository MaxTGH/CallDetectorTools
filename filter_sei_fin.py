'''
Author: MN
Date: 8/13/26

Description:
    Keeps only the selected call types from the detection file.
'''

import pandas as pd

# Input file
input_file = r"F:\Model_2\detections\raw_detections_context_filtered.txt"

# Read the tab-delimited text file
df = pd.read_csv(input_file, sep="\t")

# Keep only the desired labels
labels_to_keep = ["Bp_20Hz", "Bp_40Hz", "Bb_down-sweep"]

filtered_df = df[df["label"].isin(labels_to_keep)]

# View the filtered data
print(filtered_df)

# (Optional) Save to a new tab-delimited file
output_file = r"F:\Model_2\detections\filtered_detections.txt"
filtered_df.to_csv(output_file, sep="\t", index=False)

print(f"Saved {len(filtered_df)} detections to {output_file}")