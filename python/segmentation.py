"""User segmentation based on observed behavior."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_events() -> pd.DataFrame:
    path = PROCESSED / "events_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Run python/data_cleaning.py first.")
    return pd.read_csv(path, parse_dates=["event_time"])


def segment_users(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = (
        df.groupby("user_id")
        .agg(
            sessions=("user_session", "nunique"),
            events=("event_type", "size"),
            views=("event_type", lambda s: int(s.eq("view").sum())),
            carts=("event_type", lambda s: int(s.eq("cart").sum())),
            purchases=("event_type", lambda s: int(s.eq("purchase").sum())),
            revenue=("revenue", "sum"),
            first_seen=("event_time", "min"),
            last_seen=("event_time", "max"),
        )
        .reset_index()
    )

    def assign(row: pd.Series) -> str:
        if row["purchases"] > 0:
            return "High-value users (purchasers)"
        if row["carts"] > 0:
            return "Cart abandoners"
        if row["views"] > 0:
            return "Browsers"
        return "Inactive users"

    base["segment"] = base.apply(assign, axis=1)
    summary = (
        base.groupby("segment")
        .agg(
            users=("user_id", "nunique"),
            sessions=("sessions", "sum"),
            views=("views", "sum"),
            carts=("carts", "sum"),
            purchases=("purchases", "sum"),
            revenue=("revenue", "sum"),
        )
        .reset_index()
        .sort_values("users", ascending=False)
    )
    summary["user_share"] = summary["users"] / summary["users"].sum()
    summary["revenue_share"] = summary["revenue"] / summary["revenue"].sum()
    return base, summary


def main() -> None:
    users, summary = segment_users(load_events())
    users.to_csv(PROCESSED / "user_segments.csv", index=False)
    summary.to_csv(PROCESSED / "segment_summary.csv", index=False)
    print("Wrote segmentation outputs.")


if __name__ == "__main__":
    main()

