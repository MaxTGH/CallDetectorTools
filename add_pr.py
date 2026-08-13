'''
Author: MN

Description:
    Adds a 'pr' column with a value of 1 if it does not already exist.
'''

import pandas as pd
import os


folder = r"F:\detections\Relabeledv2"
file = "Azores_B_01_WMV.txt"

path = os.path.join(folder, file)

df = pd.read_csv(path, sep="\t")

# Clean up column names
df.columns = df.columns.str.strip()

# Only add the column if it doesn't already exist
if "pr" not in df.columns:
    df["pr"] = 1
    df.to_csv(path, sep="\t", index=False)
    print("Added 'pr' column.")
else:
    print("'pr' column already exists. No changes made.")