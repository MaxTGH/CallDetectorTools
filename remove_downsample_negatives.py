'''
Author: MN
Date: 8/13/26

Description:
    Removes annotations with missing or empty labels from make_new_examples file.
'''
import pandas as pd

# Input and output files
input_file = r"F:\Model_1\Annotations\new_examples_season.txt"
output_file = r"F:\Model_1\Annotations\new_examples_season_cleaned.txt"

# Read the file
df = pd.read_csv(input_file, sep="\t", low_memory=False)

# Keep only rows with a non-empty label
df = df[df["label"].notna()]
df = df[df["label"].astype(str).str.strip() != ""]

# Save the filtered file
df.to_csv(output_file, sep="\t", index=False)

print(f"Kept {len(df)} rows with labels.")
print(f"Saved to: {output_file}")