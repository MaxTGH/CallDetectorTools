import pandas as pd

# Input/output files
input_file = r"F:\detections\Relabeledv2\combined_detections.txt"
output_file = r"F:\detections\Relabeledv2\combined_detections_with_season.txt"

# Read the tab-delimited file
df = pd.read_csv(input_file, sep="\t")

# Convert start_time to datetime
df["start_time"] = pd.to_datetime(df["start_time"])

# Function to assign season (Northern Hemisphere)
def get_season(date):
    month = date.month

    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:  # September, October, November
        return "fall"

# Create/update the season column
df["season"] = df["start_time"].apply(get_season)

# Save the updated file
df.to_csv(output_file, sep="\t", index=False)

print(f"Updated file saved to:\n{output_file}")

# Display counts by season
print("\nSeason counts:")
print(df["season"].value_counts().sort_index())