'''
Author: MN
Date: 8/13/26

Description:
    Filters detections using species-specific score thresholds.
'''

import csv

# ------------------------------------------------------------------
# File paths
# ------------------------------------------------------------------
INPUT_FILE = r"F:\detections\Verified\verified_detections_NFC_A_04_final.txt"
OUTPUT_FILE = r"F:\detections\Verified\verified_detections_NFC_A_04_finalv2.txt"

# ------------------------------------------------------------------
# Species-specific thresholds
# ------------------------------------------------------------------
THRESHOLDS = {
    "Bm_A_North_Atlantic": 0.15,
    "Ba_pulse-call": 0.85,
    "Bp_20Hz": 0.2,
    "Bp_40Hz": 0.25,
    "Bb_down-sweep": 0.2,
}

DEFAULT_THRESHOLD = 0.0   # Used if a label is not found above
# ------------------------------------------------------------------

total = 0
kept = 0
removed_by_species = {}

with open(INPUT_FILE, "r", encoding="utf-8", newline="") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:

    reader = csv.DictReader(infile, delimiter="\t")
    writer = csv.DictWriter(
        outfile,
        fieldnames=reader.fieldnames,
        delimiter="\t"
    )

    writer.writeheader()

    for row in reader:
        total += 1

        label = row["label"]
        score = float(row["score"])

        threshold = THRESHOLDS.get(label, DEFAULT_THRESHOLD)

        if score >= threshold:
            writer.writerow(row)
            kept += 1
        else:
            removed_by_species[label] = removed_by_species.get(label, 0) + 1

print(f"Total detections : {total:,}")
print(f"Kept detections  : {kept:,}")
print(f"Removed          : {total-kept:,}")

print("\nRemoved by species:")
for species, count in sorted(removed_by_species.items()):
    print(f"  {species:<25} {count:,}")

print(f"\nFiltered detections written to:\n{OUTPUT_FILE}")