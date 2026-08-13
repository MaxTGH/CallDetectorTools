'''
Author: MN
Date: 8/13/26

Description:
    Counts each call type across all detection files in a folder.
'''

import os
import glob
import pandas as pd


def count_call_types(folder_path, output_csv=None):
    """
    Count occurrences of each call type in the 'label' column across all
    tab-delimited .txt detection files in a folder.
    """

    # Find all .txt files in the folder
    file_paths = glob.glob(os.path.join(folder_path, "*.txt"))

    if not file_paths:
        raise ValueError(f"No .txt files found in {folder_path}")

    all_counts = []

    for file_path in file_paths:
        df = pd.read_csv(file_path, sep="\t")

        if "label" not in df.columns:
            print(f"Skipping {os.path.basename(file_path)} (no 'label' column)")
            continue

        counts = (
            df["label"]
            .value_counts()
            .rename_axis("call_type")
            .reset_index(name="count")
        )

        counts["file"] = os.path.basename(file_path)
        all_counts.append(counts)

    combined = pd.concat(all_counts, ignore_index=True)

    summary = (
        combined
        .groupby("call_type", as_index=False)["count"]
        .sum()
        .sort_values("count", ascending=False)
    )

    print("\nCounts by file:")
    print(combined.to_string(index=False))

    print("\nTotal counts across all files:")
    print(summary.to_string(index=False))

    if output_csv is not None:
        summary.to_csv(output_csv, index=False)
        print(f"\nCounts saved to: {output_csv}")

    return combined, summary


# Folder containing your detection files
folder = r"F:\detections"

# Optional: save summary to CSV
output_file = os.path.join(folder, "call_type_summary.csv")

counts_by_file, total_counts = count_call_types(
    folder,
    output_csv=output_file
)