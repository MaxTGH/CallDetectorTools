'''
Author: MN
Date: 8/13/26

Description:
    Combines two detection files and sorts them by start time.
'''

import pandas as pd

# Input files
file1 = r"F:\Model_2\detections\context_seifin_filtered_detections.txt"
file2 = r"C:\Users\DAM_1\Downloads\NFC_A_03_MFA_WMVZ.txt"

# Read both tab-delimited files
df1 = pd.read_csv(file1, sep="\t")
df2 = pd.read_csv(file2, sep="\t")

# Combine
combined = pd.concat([df1, df2], ignore_index=True)

# Sort by start_time
combined["start_time"] = pd.to_datetime(combined["start_time"])
combined = combined.sort_values("start_time").reset_index(drop=True)

# Save
output_file = r"F:\Model_2\detections\combined_sorted_detections.txt"
combined.to_csv(output_file, sep="\t", index=False)

print(f"Combined {len(combined)} detections.")
print(f"Saved to {output_file}")