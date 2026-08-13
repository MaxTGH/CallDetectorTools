'''
Author: MN
Date: 8/13/26

Description:
    Relabels detection labels using a predefined label map and removes
    unwanted call types from all detection files. Also removes Bp_40Hz
    detections from specified deployments and saves the cleaned files
    to the Relabeledv2 folder.
'''


import os
import glob
import pandas as pd





# Main detections folder
base_folder = r"F:\detections"

# Input .txt files are inside Raw
input_folder = os.path.join(base_folder, "Raw_verified_v2")

# Save relabeled files inside Relabeled
output_folder = os.path.join(base_folder, "Relabeledv2")
os.makedirs(output_folder, exist_ok=True)

LABEL_MAP = {
    "40Hz": "Bp_40Hz",
    "Downsweep": "Bb_down-sweep",
    "Pulse_train": "Ba_pulse-call",
    "Bm_B_North_Atlantic": "Bm_A_North_Atlantic",
    "Bm_AB_North_Atlantic": "Bm_A_North_Atlantic",
    "A N Atlantic": "Bm_A_North_Atlantic"
}

LABELS_TO_REMOVE = {
    "Bm_arch",
    "Up-call",
    "NARW_up-call"
}

txt_files = glob.glob(os.path.join(input_folder, "*.txt"))

print(f"Looking for .txt files in: {input_folder}")
print(f"Found {len(txt_files)} .txt files.")

for input_file in txt_files:
    print(f"\nProcessing {os.path.basename(input_file)}...")

    df = pd.read_csv(input_file, sep="\t")

    if "label" not in df.columns:
        print("  Skipped: no 'label' column found.")
        continue

    # Clean label text first
    df["label"] = df["label"].astype(str).str.strip()

    # Replace labels
    df["label"] = df["label"].replace(LABEL_MAP)

    # Remove unwanted labels
    rows_before = len(df)
    df = df[~df["label"].isin(LABELS_TO_REMOVE)]
    rows_removed = rows_before - len(df)

    

    print(f"  Removed {rows_removed} rows.")

    # Remove all Bp_40Hz detections from Azores_B_01_WMV.txt
    if os.path.basename(input_file) == "Azores_B_01_WMV.txt":
        rows_before = len(df)
        df = df[df["label"] != "Bp_40Hz"]
        print(f"  Removed {rows_before - len(df)} Bp_40Hz detections from Azores_B_01_WMV.txt")

    # Remove all Bp_40Hz detections from HAT02A_allLF_cleaned_CMSS_verified.txt
    if os.path.basename(input_file) == "HAT02A_allLF_cleaned_CMSS_verified.txt":
        rows_before = len(df)
        df = df[df["label"] != "Bp_40Hz"]
        print(f"  Removed {rows_before - len(df)} Bp_40Hz detections from HAT02A_allLF_cleaned_CMSS_verified.txt")

    output_file = os.path.join(output_folder, os.path.basename(input_file))
    df.to_csv(output_file, sep="\t", index=False)

    print(f"  Saved to {output_file}")

print("\nFinished processing all files.")