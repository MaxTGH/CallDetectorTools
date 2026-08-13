'''
Author: MN
Date: 8/13/26

Description:
    Summarizes call counts and the number of spectrograms containing each
    call type, including images with single or multiple call types.
'''

import pandas as pd

TRAIN_SPLIT = r"F:\Model_3\annotations\Splits_80_10_10\train_filtered.txt"

df = pd.read_csv(TRAIN_SPLIT, sep="\t")

# Labels present in each spectrogram
image_labels = (
    df.groupby("spectrogram_path")["label"]
      .apply(lambda x: set(x))
)

results = []

for label in sorted(df["label"].unique()):
    contains_label = image_labels.apply(lambda s: label in s)
    only_label = image_labels.apply(lambda s: s == {label})

    results.append({
        "Label": label,
        "Calls": (df["label"] == label).sum(),
        "Images containing label": contains_label.sum(),
        "Images with only this label": only_label.sum(),
        "Images with multiple labels": contains_label.sum() - only_label.sum(),
    })

summary = pd.DataFrame(results).sort_values("Calls")

print(summary.to_string(index=False))