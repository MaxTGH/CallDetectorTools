'''
Author: MN
Date: 8/13/26

Description:
    Balances the dataset by sampling up to 2,000 detections per call type.
    Sampling is distributed across seasons and deployments while preserving
    smaller groups and proportionally sampling from larger groups.
'''

import pandas as pd
import numpy as np


# -----------------------------------------------------------
# Utility: hierarchical proportional allocation
# -----------------------------------------------------------

def allocate_counts(counts, target):
    """
    Allocate an integer sample size across groups while
    preserving all small groups.

    Parameters
    ----------
    counts : pandas Series
        index = group names
        values = counts
    target : int

    Returns
    -------
    pandas Series
        allocated sample size for each group
    """

    counts = counts.sort_values()

    allocation = pd.Series(0, index=counts.index, dtype=int)

    remaining_groups = counts.copy()
    remaining_target = target

    while True:

        if len(remaining_groups) == 0:
            break

        average_allowed = remaining_target / len(remaining_groups)

        small = remaining_groups[remaining_groups <= average_allowed]

        if len(small) == 0:
            break

        allocation.loc[small.index] = small

        remaining_target -= small.sum()

        remaining_groups = remaining_groups.drop(small.index)

    if len(remaining_groups):

        proportional = (
            remaining_groups / remaining_groups.sum() * remaining_target
        )

        floors = np.floor(proportional).astype(int)

        allocation.loc[floors.index] = floors

        leftover = remaining_target - floors.sum()

        if leftover > 0:
            remainders = proportional - floors

            winners = remainders.sort_values(
                ascending=False
            ).index[:leftover]

            allocation.loc[winners] += 1

    return allocation.astype(int)


# -----------------------------------------------------------
# Sample one season
# -----------------------------------------------------------

def sample_season(df_season, target, deployment_col,
                  random_state=42):

    dep_counts = df_season[deployment_col].value_counts()

    allocation = allocate_counts(dep_counts, target)

    sampled = []

    for dep, n in allocation.items():

        subset = df_season[df_season[deployment_col] == dep]

        if n >= len(subset):
            sampled.append(subset)
        else:
            sampled.append(
                subset.sample(
                    n=n,
                    random_state=random_state
                )
            )

    return pd.concat(sampled)


# -----------------------------------------------------------
# Sample one call type
# -----------------------------------------------------------

def sample_call_type(df_call,
                     target,
                     season_col,
                     deployment_col,
                     random_state=42):

    if len(df_call) <= target:
        return df_call

    season_counts = df_call[season_col].value_counts()

    season_allocation = allocate_counts(
        season_counts,
        target
    )

    sampled = []

    for season, n in season_allocation.items():

        season_df = df_call[
            df_call[season_col] == season
        ]

        sampled.append(
            sample_season(
                season_df,
                n,
                deployment_col,
                random_state
            )
        )

    return pd.concat(sampled)


# -----------------------------------------------------------
# Entire dataset
# -----------------------------------------------------------

def balance_dataset(
        input_file,
        output_file,
        target_per_call=2000,
        label_col="label",
        season_col="season",
        deployment_col="source_txt_file",
        random_state=42):

    # Read data
    df = pd.read_csv(
        input_file,
        sep="\t"
    )

    print("\n==============================")
    print("BEFORE SAMPLING")
    print("==============================")

    print("\nCounts by call type\n")
    print(df[label_col].value_counts())

    print("\nCounts by season\n")
    print(
        pd.crosstab(
            df[label_col],
            df[season_col]
        )
    )

    print("\nCounts by deployment\n")
    print(
        pd.crosstab(
            df[label_col],
            df[deployment_col]
        )
    )

    balanced = []

    for label, subset in df.groupby(label_col):

        print(
            f"\nProcessing {label}: "
            f"{len(subset)} detections"
        )

        balanced.append(
            sample_call_type(
                subset,
                target_per_call,
                season_col,
                deployment_col,
                random_state
            )
        )

    balanced = (
        pd.concat(balanced)
        .sort_index()
    )

    print("\n==============================")
    print("AFTER SAMPLING")
    print("==============================")

    print("\nCounts by call type\n")
    print(
        balanced[label_col].value_counts()
    )

    print("\nCounts by season\n")
    print(
        pd.crosstab(
            balanced[label_col],
            balanced[season_col]
        )
    )

    print("\nCounts by deployment\n")
    print(
        pd.crosstab(
            balanced[label_col],
            balanced[deployment_col]
        )
    )

    balanced.to_csv(
        output_file,
        sep="\t",
        index=False
    )

    print(f"\nSaved balanced dataset to:\n{output_file}")


# -----------------------------------------------------------
# Example
# -----------------------------------------------------------

if __name__ == "__main__":

    balance_dataset(
        input_file="F:\detections\Relabeledv2\combined_detections_with_season.txt",
        output_file="F:\detections\Relabeledv2\combined_detections_with_season_balanced.txt",
        target_per_call=2000,
        label_col="label",
        season_col="season",
        deployment_col="source_txt_file",
        random_state=42,
    )