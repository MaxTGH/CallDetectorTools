'''
Author: MN
Date: 8/13/26

Description:
    Filters detection files to keep only rows where pr equals 1.
'''

from pathlib import Path
import pandas as pd

# Input and output folders
input_dir = Path(r"F:\detections\raw")
output_dir = Path(r"F:\detections\filtered_pr_unnecessary")

# Create output folder if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Process all .txt and .tsv files
for file in list(input_dir.glob("*.txt")) + list(input_dir.glob("*.tsv")):
    try:
        # Read tab-delimited file
        df = pd.read_csv(file, sep="\t")

        # Skip files without a 'pr' column
        if "pr" not in df.columns:
            print(f"Skipping {file.name}: no 'pr' column")
            continue

        # Filter rows where pr == 1
        filtered_df = df[df["pr"] == 1]

        # Save to output folder
        output_file = output_dir / file.name
        filtered_df.to_csv(output_file, sep="\t", index=False)

        print(f"Processed: {file.name}")

    except Exception as e:
        print(f"Error processing {file.name}: {e}")

print("Done!")