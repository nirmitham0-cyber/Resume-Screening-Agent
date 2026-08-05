import os
import json
import pandas as pd


OUTPUT_FOLDER = "output"


def export_results(results):
    """
    Save ranked results to CSV and JSON.

    Parameters
    ----------
    results : list
        List of candidate dictionaries.
    """

    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # ----------------------------
    # Export CSV
    # ----------------------------
    csv_file = os.path.join(
        OUTPUT_FOLDER,
        "ranked_candidates.csv"
    )

    df = pd.DataFrame(results)

    df.to_csv(
        csv_file,
        index=False,
        encoding="utf-8"
    )

    # ----------------------------
    # Export JSON
    # ----------------------------
    json_file = os.path.join(
        OUTPUT_FOLDER,
        "ranked_candidates.json"
    )

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResults exported successfully.")
    print(f"CSV  : {csv_file}")
    print(f"JSON : {json_file}")