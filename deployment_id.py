'''
Author: MN
Date: 8/13/26

Description:
    Adds a deployment ID based on each spectrogram filename.
'''

import os
import glob
import pandas as pd

# Folder containing annotation files
input_folder = r"F:\Model_3\annotations"

deployment_list = [
    "AZORES_B_01",
    "HAT02A",
    "HAT_A_06",
    "NFC_A_02",
    "NFC_A_04",
    "NFC_A_03"
]

def get_deployment_id(path):
    """
    Extract deployment ID from the spectrogram path.
    """
    path = str(path).replace("\\", "/")
    filename = os.path.basename(path).upper()

    for deployment in deployment_list:
        if filename.startswith(deployment.upper()):
            return deployment

    return None

# Process every txt file
txt_files = glob.glob(os.path.join(input_folder, "*.txt"))

for input_file in txt_files:

    print(f"Processing {os.path.basename(input_file)}...")

    df = pd.read_csv(input_file, sep="\t", low_memory=False)

    if "spectrogram_path" not in df.columns:
        print("  Skipped: no 'spectrogram_path' column found.")
        continue

    # Create deployment_id column
    df["deployment_id"] = df["spectrogram_path"].apply(get_deployment_id)

    # Save as a new file in the same folder
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_with_deployment_id{ext}"

    df.to_csv(output_file, sep="\t", index=False)

    print(f"  Saved to {output_file}")

    # Print deployment counts
    print(df["deployment_id"].value_counts(dropna=False).sort_index())

print("\nFinished.")