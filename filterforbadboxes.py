'''
Author: MN
Date: 8/13/26

Description:
    Removes annotations with invalid bounding boxes.
'''

import pandas as pd

input_file = r"F:\Model_3\annotations\Splits_80_10_10\train.txt"
output_file = r"F:\Model_3\annotations\Splits_80_10_10\train_filtered.txt"

df = pd.read_csv(input_file, sep="\t", low_memory=False)

# Find invalid bounding boxes
bad = df[(df["xmin"] >= df["xmax"]) | (df["ymin"] >= df["ymax"])]

print(f"Found {len(bad)} invalid annotations.\n")

if not bad.empty:
    # Add row numbers from the original file
    bad = bad.reset_index().rename(columns={"index": "row_number"})
    print(bad[[
        "row_number",
        "spectrogram_path",
        "label",
        "xmin",
        "xmax",
        "ymin",
        "ymax"
    ]])

# Keep only valid bounding boxes
df = df[(df["xmin"] < df["xmax"]) & (df["ymin"] < df["ymax"])]

df.to_csv(output_file, sep="\t", index=False)

print(f"\nRemaining annotations: {len(df)}")
print(f"Saved filtered annotations to:\n{output_file}")