'''
Author: MN
Date: 8/13/26

Description:
    Compares the number of spectrogram PNGs with unique annotation entries.
'''

from pathlib import Path
import pandas as pd

# Paths
spectrogram_folder = Path(r"F:\Model_2\spectrograms")
annotation_file = r"F:\Model_2\Annotations\new_examples_untouched.txt"

# Count PNG files in the spectrogram folder
png_count = len(list(spectrogram_folder.glob("*.png")))

# Read the tab-delimited annotation file
df = pd.read_csv(annotation_file, sep="\t")

# Count unique spectrogram_path entries
unique_spectrograms = df["spectrogram_path"].nunique()

# Print results
print(f"PNG files in folder: {png_count}")
print(f"Unique spectrogram_path entries: {unique_spectrograms}")

# Compare the counts
if png_count == unique_spectrograms:
    print("✅ Counts match.")
else:
    print(f"❌ Counts do not match. Difference: {png_count - unique_spectrograms}")