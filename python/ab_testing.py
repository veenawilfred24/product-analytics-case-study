"""A/B testing simulation using real observed user conversion outcomes.

Only assignment is simulated. Conversion outcomes come from the provided dataset.
"""

from __future__ import annotations

from pathlib import Path
import math

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def two_proportion_z_test(control_conversions: int, control_users: int, treatment_conversions: int, treatment_users: int) -> dict:
    p_control = control_conversions / control_users
    p_treatment = treatment_conversions / treatment_users
    pooled = (control_conversions + treatment_conversions) / (control_users + treatment_users)
    se = math.sqrt(pooled * (1 - pooled) * (1 / control_users + 1 / treatment_users))
    z_score = (p_treatment - p_control) / se if se else 0
    p_value = 2 * (1 - normal_cdf(abs(z_score)))
    return {
        "control_conversion_rate": p_control,
        "treatment_conversion_rate": p_treatment,
        "absolute_lift": p_treatment - p_control,
        "relative_lift": (p_treatment / p_control) - 1 if p_control else float("nan"),
        "z_score": z_score,
        "p_value": p_value,
        "significant_at_05": p_value < 0.05,
    }


def run_experiment(seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    events_path = PROCESSED / "events_clean.csv"
    if not events_path.exists():
        raise FileNotFoundError("Run python/data_cleaning.py first.")
    df = pd.read_csv(events_path)
    users = pd.DataFrame({"user_id": sorted(df["user_id"].unique())})
    rng = np.random.default_rng(seed)
    users["variant"] = rng.choice(["A", "B"], size=len(users), p=[0.5, 0.5])
    purchasers = set(df.loc[df["event_type"].eq("purchase"), "user_id"])
    users["converted"] = users["user_id"].isin(purchasers)

    summary = (
        users.groupby("variant")
        .agg(users=("user_id", "nunique"), converted_users=("converted", "sum"), conversion_rate=("converted", "mean"))
        .reset_index()
    )
    a = summary.loc[summary["variant"].eq("A")].iloc[0]
    b = summary.loc[summary["variant"].eq("B")].iloc[0]
    test = two_proportion_z_test(int(a["converted_users"]), int(a["users"]), int(b["converted_users"]), int(b["users"]))
    test_summary = pd.DataFrame([{"metric": key, "value": value} for key, value in test.items()])
    return summary, test_summary


def main() -> None:
    summary, test_summary = run_experiment()
    summary.to_csv(PROCESSED / "ab_test_variant_summary.csv", index=False)
    test_summary.to_csv(PROCESSED / "ab_test_results.csv", index=False)
    print("Wrote A/B testing outputs.")


if __name__ == "__main__":
    main()

