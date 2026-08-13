'''
Author: MN
Date: 8/13/26

Description:
    Creates frequency and duration histograms for each call type.
'''

import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# User settings
# ----------------------------

csv_file = "F:/detections/Relabeled_cleaned/combined_detections.txt"

label_map = {
    'Bm_A_North_Atlantic': 1,
    'Ba_pulse-call': 2,
    'Bp_20Hz': 3,
    'Bp_40Hz': 4,
    'Bb_down-sweep': 5
}

output_dir = "call_histograms"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# Load data
# ----------------------------

df = pd.read_csv(csv_file, sep="\t")

# Convert timestamps
df["start_time"] = pd.to_datetime(df["start_time"])
df["end_time"] = pd.to_datetime(df["end_time"])

# Compute duration (seconds)
df["duration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()

# ----------------------------
# Plot histograms
# ----------------------------

for label in label_map.keys():

    subset = df[df["label"] == label]

    if subset.empty:
        print(f"No detections for {label}")
        continue

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Minimum frequency
    axes[0].hist(subset["min_frequency"].dropna(), bins=25)
    axes[0].set_title("Minimum Frequency")
    axes[0].set_xlabel("Frequency (Hz)")
    axes[0].set_ylabel("Count")

    # Maximum frequency
    axes[1].hist(subset["max_frequency"].dropna(), bins=25)
    axes[1].set_title("Maximum Frequency")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Count")

    # Duration
    axes[2].hist(subset["duration"].dropna(), bins=25)
    axes[2].set_title("Call Duration")
    axes[2].set_xlabel("Duration (s)")
    axes[2].set_ylabel("Count")

    fig.suptitle(label)

    plt.tight_layout()

    save_path = os.path.join(output_dir, f"{label}_histograms.png")
    plt.savefig(save_path, dpi=300)
    plt.close(fig)

    print(f"Saved {save_path}")

print("Done.")