'''
Author: MN
Date: 8/13/26

Description:
    Keeps only detections occurring before a specified cutoff time.
'''

import pandas as pd

input_file = r"F:\detections\Raw_verified\NFC_A_02_verified_Ba_NFC_A_02_spring_MN_edits_CMS_edits_partial.txt"
output_file = r"F:\detections\Raw_verified\NFC_A_02_verified_Ba_NFC_A_02_spring_MN_edits_CMS_edits_partial_before20170402_100353.txt"

# Read tab-delimited file
df = pd.read_csv(input_file, sep="\t")

# Convert start_time to datetime
df["start_time"] = pd.to_datetime(
    df["start_time"],
    format="%Y-%m-%d %H:%M:%S.%f"
)

# Keep only detections before 2017-04-02 10:04:53
cutoff = pd.Timestamp("2017-04-02 10:03:53")
df = df[df["start_time"] < cutoff]

# Convert back to original format
df["start_time"] = df["start_time"].dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]

# Save
df.to_csv(output_file, sep="\t", index=False)

print(f"Saved {len(df)} detections to:")
print(output_file)