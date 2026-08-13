'''
Author: MN
Date: 8/13/26

Description:
    Keeps only February, March, and April detections.
'''

import pandas as pd

# Input and output files
input_file = r"F:\Model_1\detections\verified_detections_NFC_A_03.txt"
output_file = r"F:\Model_1\detections\verified_detections_NFC_A_03_spring.txt"

# Read the tab-delimited file
df = pd.read_csv(input_file, sep="\t", parse_dates=["start_time"])

# Keep only February, March, and April detections
spring_detections = df[df["start_time"].dt.month.isin([2, 3, 4])]

# Save as a tab-delimited file
spring_detections.to_csv(output_file, sep="\t", index=False)

print(f"Saved {len(spring_detections)} spring detections to:")
print(output_file)