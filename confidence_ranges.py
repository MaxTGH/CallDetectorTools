'''
Author: MN
Date: 8/13/26

Description:
    Summarizes confidence scores for true and false positive detections.
'''

import pandas as pd

# ----------------------------
# User settings
# ----------------------------

csv_file = r"F:\detections\Verified\verified_detections_NFC_A_04_spring.txt"

# Analysis window
start_date = "2019-02-01 00:00:00"
end_date = "2019-02-01 02:19:17"   # Change as needed

# Label mapping
label_map = {
    'Bm_A_North_Atlantic': 1,
    'Ba_pulse-call': 2,
    'Bp_20Hz': 3,
    'Bp_40Hz': 4,
    'Bb_down-sweep': 5
}

# ----------------------------
# Load data
# ----------------------------

df = pd.read_csv(csv_file, sep="\t")

# Convert start_time to datetime
df["start_time"] = pd.to_datetime(df["start_time"])

# Filter by date
df = df[
    (df["start_time"] >= pd.to_datetime(start_date)) &
    (df["start_time"] <= pd.to_datetime(end_date))
]

# ----------------------------
# Summarize confidence ranges
# ----------------------------

results = []

for label in label_map.keys():

    label_df = df[df["label"] == label]

    for pr_value, pr_name in [
        (1, "True Positive"),
        (2, "False Positive")
    ]:

        subset = label_df[label_df["pr"] == pr_value]

        results.append({
            "Label": label,
            "Class ID": label_map[label],
            "Category": pr_name,
            "Count": len(subset),
            "Min Confidence": subset["score"].min() if not subset.empty else None,
            "Max Confidence": subset["score"].max() if not subset.empty else None,
            "Mean Confidence": subset["score"].mean() if not subset.empty else None,
            "Median Confidence": subset["score"].median() if not subset.empty else None,
        })

results_df = pd.DataFrame(results)

print(results_df)

# Save results
results_df.to_csv("confidence_ranges.csv", index=False)