"""Ordered funnel analysis: view -> cart -> purchase."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_events() -> pd.DataFrame:
    path = PROCESSED / "events_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Run python/data_cleaning.py first.")
    df = pd.read_csv(path, parse_dates=["event_time"])
    return df.sort_values("event_time")


def ordered_funnel(df: pd.DataFrame, entity: str = "user_id") -> pd.DataFrame:
    rows = []
    for key, group in df.groupby(entity):
        group = group.sort_values("event_time")
        view_time = group.loc[group["event_type"].eq("view"), "event_time"].min()
        if pd.isna(view_time):
            continue
        cart_time = group.loc[
            group["event_type"].eq("cart") & group["event_time"].ge(view_time), "event_time"
        ].min()
        purchase_time = (
            group.loc[group["event_type"].eq("purchase") & group["event_time"].ge(cart_time), "event_time"].min()
            if pd.notna(cart_time)
            else pd.NaT
        )
        rows.append(
            {
                entity: key,
                "view": True,
                "cart": pd.notna(cart_time),
                "purchase": pd.notna(purchase_time),
            }
        )
    return pd.DataFrame(rows)


def summarize_funnel(funnel: pd.DataFrame) -> pd.DataFrame:
    view_users = int(funnel["view"].sum())
    cart_users = int(funnel["cart"].sum())
    purchase_users = int(funnel["purchase"].sum())
    rows = [
        {
            "stage": "view",
            "users": view_users,
            "stage_conversion_rate": 1.0,
            "overall_conversion_rate": 1.0,
            "dropoff_from_previous_stage": 0.0,
        },
        {
            "stage": "cart",
            "users": cart_users,
            "stage_conversion_rate": cart_users / view_users if view_users else 0,
            "overall_conversion_rate": cart_users / view_users if view_users else 0,
            "dropoff_from_previous_stage": 1 - (cart_users / view_users if view_users else 0),
        },
        {
            "stage": "purchase",
            "users": purchase_users,
            "stage_conversion_rate": purchase_users / cart_users if cart_users else 0,
            "overall_conversion_rate": purchase_users / view_users if view_users else 0,
            "dropoff_from_previous_stage": 1 - (purchase_users / cart_users if cart_users else 0),
        },
    ]
    return pd.DataFrame(rows)


def category_funnel(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for category, group in df.groupby("category_l1"):
        funnel = ordered_funnel(group)
        if funnel.empty:
            continue
        summary = summarize_funnel(funnel)
        view_users = int(summary.loc[summary["stage"].eq("view"), "users"].iloc[0])
        if view_users < 50:
            continue
        cart_users = int(summary.loc[summary["stage"].eq("cart"), "users"].iloc[0])
        purchase_users = int(summary.loc[summary["stage"].eq("purchase"), "users"].iloc[0])
        revenue = group.loc[group["event_type"].eq("purchase"), "revenue"].sum()
        rows.append(
            {
                "category_l1": category,
                "view_users": view_users,
                "cart_users": cart_users,
                "purchase_users": purchase_users,
                "view_to_cart_rate": cart_users / view_users if view_users else 0,
                "cart_to_purchase_rate": purchase_users / cart_users if cart_users else 0,
                "view_to_purchase_rate": purchase_users / view_users if view_users else 0,
                "purchase_revenue": revenue,
            }
        )
    return pd.DataFrame(rows).sort_values("view_to_purchase_rate", ascending=False)


def hourly_funnel(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for hour, group in df.groupby("event_hour"):
        funnel = ordered_funnel(group)
        summary = summarize_funnel(funnel)
        rows.append(
            {
                "event_hour": hour,
                "view_users": int(summary.loc[summary["stage"].eq("view"), "users"].iloc[0]),
                "cart_users": int(summary.loc[summary["stage"].eq("cart"), "users"].iloc[0]),
                "purchase_users": int(summary.loc[summary["stage"].eq("purchase"), "users"].iloc[0]),
                "view_to_purchase_rate": float(
                    summary.loc[summary["stage"].eq("purchase"), "overall_conversion_rate"].iloc[0]
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("event_hour")


def main() -> None:
    df = load_events()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    user_funnel = ordered_funnel(df)
    summarize_funnel(user_funnel).to_csv(PROCESSED / "funnel_summary.csv", index=False)
    category_funnel(df).to_csv(PROCESSED / "funnel_by_category.csv", index=False)
    hourly_funnel(df).to_csv(PROCESSED / "funnel_by_hour.csv", index=False)
    ordered_funnel(df, entity="user_session").to_csv(PROCESSED / "session_funnel_flags.csv", index=False)
    print("Wrote funnel analysis outputs.")


if __name__ == "__main__":
    main()

