'''
Author: MN
Date: 8/13/26

Description:
    Creates a rough (estimate) precision-recall curves for each call type from model evaluation
    results. Each point is labeled with its corresponding score threshold
    to show how precision and recall change across confidence thresholds.
'''

from pathlib import Path
import matplotlib.pyplot as plt
import re

# Text file
txt_file = Path(
    r"F:\Model_2\eval\Atlantic_model2_MN_classWeighting\test_filtered_Atlantic_model2_MN_classWeighting_10_percent_iou_v2.txt"
)

data = {}

print(f"Reading {txt_file.name}")

current_threshold = None

with open(txt_file, "r") as f:
    for line in f:

        line = line.strip()

        # Find threshold
        m = re.search(r"Score Threshold\s*=\s*([0-9.]+)", line)
        if m:
            current_threshold = float(m.group(1))
            continue

        # Find precision/recall lines
        m = re.search(
            r"(.+?)\s*\|\s*Precision:\s*([0-9.]+)\s*\|\s*Recall:\s*([0-9.]+)",
            line,
        )

        if m:

            call_type = m.group(1).strip()
            precision = float(m.group(2))
            recall = float(m.group(3))

            data.setdefault(call_type, {
                "precision": [],
                "recall": [],
                "threshold": []
            })

            data[call_type]["precision"].append(precision)
            data[call_type]["recall"].append(recall)
            data[call_type]["threshold"].append(current_threshold)

# ==========================================================
# Plot
# ==========================================================

plt.figure(figsize=(10,8))

markers = ['o','s','^','D','P','X','v','*']

for i, (call_type, values) in enumerate(sorted(data.items())):

    recall = values["recall"]
    precision = values["precision"]
    thresholds = values["threshold"]

    plt.plot(
        recall,
        precision,
        marker=markers[i % len(markers)],
        linewidth=2,
        markersize=6,
        label=call_type,
    )

    # Label each point with threshold
    for r, p, t in zip(recall, precision, thresholds):
        plt.annotate(
            f"{t:.1f}",
            (r, p),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curves by Call Type")
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

outfile = txt_file.with_name("precision_recall_curves.png")
plt.savefig(outfile, dpi=300)

plt.show()

print(f"\nSaved to:\n{outfile}")