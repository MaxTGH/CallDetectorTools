'''
Author: MN
Date: 7/14/26

Description:
    Combines detection files and records their source file for make_new_examples (whalemoandetector)
'''


import os
import glob
import pandas as pd

# Folder containing the .txt files
input_folder = r"F:\detections\Relabeledv2"

# Output file
output_file = os.path.join(input_folder, "combined_detections.txt")

# Find all txt files
txt_files = glob.glob(os.path.join(input_folder, "*.txt"))

dfs = []

for txt_file in txt_files:
    print(f"Reading {os.path.basename(txt_file)}")

    df = pd.read_csv(txt_file, sep="\t")

    # Optional: keep track of which file each row came from
    df["source_txt_file"] = os.path.basename(txt_file)

    dfs.append(df)

# Combine all files
combined_df = pd.concat(dfs, ignore_index=True)

# Save
combined_df.to_csv(output_file, sep="\t", index=False)

print(f"\nCombined {len(txt_files)} files.")
print(f"Total detections: {len(combined_df)}")
print(f"Saved to: {output_file}")