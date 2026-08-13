'''
Author: MN
Date: 8/13/26

Description:
    Splits annotations into 80% training, 10% validation, and 10% test sets
    while stratifying by deployment, call type, and season. Groups with fewer
    than 10 detections are kept entirely in the training set. Summary counts
    are reported to verify the distribution across each split.
'''

import os
import pandas as pd
from sklearn.model_selection import train_test_split

input_file = r"F:\Model_3\annotations\new_examples_deployment_season.txt"

output_folder = r"F:\Model_3\annotations\Splits_80_10_10"
os.makedirs(output_folder, exist_ok=True)

random_seed = 42

train_dfs = []
val_dfs = []
test_dfs = []

file_name = os.path.basename(input_file)
print(f"\nProcessing {file_name}...")

df = pd.read_csv(input_file, sep="\t", low_memory=False)

required_columns = ["label", "season", "deployment_id", "spectrogram_path"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"No '{col}' column found.")

df["deployment_id"] = df["deployment_id"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()
df["season"] = df["season"].astype(str).str.strip()

for (deployment, label, season), group in df.groupby(["deployment_id", "label", "season"]):
    n = len(group)

    if n < 10:
        print(
            f"  Warning: {deployment} | {label} ({season}) "
            f"has only {n} detections. Assigning all to training."
        )
        train_dfs.append(group)
        continue

    train_group, temp_group = train_test_split(
        group,
        test_size=0.20,
        random_state=random_seed,
        shuffle=True
    )

    val_group, test_group = train_test_split(
        temp_group,
        test_size=0.50,
        random_state=random_seed,
        shuffle=True
    )

    train_dfs.append(train_group)
    val_dfs.append(val_group)
    test_dfs.append(test_group)

train_df = pd.concat(train_dfs, ignore_index=True)
val_df = pd.concat(val_dfs, ignore_index=True)
test_df = pd.concat(test_dfs, ignore_index=True)

# Save outputs
train_output = os.path.join(output_folder, "train.txt")
val_output = os.path.join(output_folder, "validation.txt")
test_output = os.path.join(output_folder, "test.txt")

train_df.to_csv(train_output, sep="\t", index=False)
val_df.to_csv(val_output, sep="\t", index=False)
test_df.to_csv(test_output, sep="\t", index=False)

print("\nFinished splitting file.")
print(f"Train saved to: {train_output}")
print(f"Validation saved to: {val_output}")
print(f"Test saved to: {test_output}")

print("\n========== LABEL COUNTS ==========")

print("\nTrain:")
print(train_df["label"].value_counts().sort_index())

print("\nValidation:")
print(val_df["label"].value_counts().sort_index())

print("\nTest:")
print(test_df["label"].value_counts().sort_index())

print("\n========== SEASON COUNTS ==========")

print("\nTrain:")
print(train_df["season"].value_counts().sort_index())

print("\nValidation:")
print(val_df["season"].value_counts().sort_index())

print("\nTest:")
print(test_df["season"].value_counts().sort_index())

print("\n========== DEPLOYMENT COUNTS ==========")

print("\nTrain:")
print(train_df["deployment_id"].value_counts().sort_index())

print("\nValidation:")
print(val_df["deployment_id"].value_counts().sort_index())

print("\nTest:")
print(test_df["deployment_id"].value_counts().sort_index())

print("\n========== DEPLOYMENT × SEASON × LABEL ==========")

summary = pd.concat([
    train_df.groupby(["deployment_id", "season", "label"]).size().rename("Train"),
    val_df.groupby(["deployment_id", "season", "label"]).size().rename("Validation"),
    test_df.groupby(["deployment_id", "season", "label"]).size().rename("Test"),
], axis=1).fillna(0).astype(int)

summary["Total"] = summary.sum(axis=1)

print(summary)