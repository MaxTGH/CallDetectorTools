'''
Author: MN
Date: 8/13/26

Description:
    Removes a specified source file and appends updated detection records.
'''


import pandas as pd

# File paths
main_file = r"F:\detections\Relabeledv2\combined_detections_MN_reviewed_filtered.txt"
append_file = r"C:\Users\DAM_1\Downloads\NFC_A_02_verified_Ba_NFC_A_02_spring_MN_edits_CMS_timetest.txt"
output_file = r"F:\detections\Relabeledv2\combined_detections_MN_reviewed_filtered_updated.txt"

# Read the tab-delimited files
main_df = pd.read_csv(main_file, sep="\t")
append_df = pd.read_csv(append_file, sep="\t")

# Remove rows with the specified source_txt_file
remove_source = (
    "NFC_A_02_verified_Ba_NFC_A_02_spring_MN_edits_CMS_edits_partial_before20170402_100453.txt"
)

# Number of rows in the original file
print(f"Original rows: {len(main_df):,}")

main_df = main_df[
    main_df["source_txt_file"] != remove_source
]
print(f"Rows after removing '{remove_source}': {len(main_df):,}")

# Set the source_txt_file for all appended rows
append_df["source_txt_file"] = (
    "NFC_A_02_verified_Ba_NFC_A_02_spring_MN_edits_CMS_timetest.txt"
)

# Append the new rows
combined_df = pd.concat([main_df, append_df], ignore_index=True)

# Display counts of source_txt_file
print("\nCounts by source_txt_file:")
print(
    combined_df["source_txt_file"]
    .value_counts()
    .sort_index()
)

# Display counts of labels
print("\nCounts by label:")
print(
    combined_df["label"]
    .value_counts()
    .sort_index()
)




# Final number of rows
print(f"Final rows: {len(combined_df):,}")