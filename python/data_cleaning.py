"""Clean the provided e-commerce event dataset.

Input:  data/sample/sample_data.csv
Output: data/processed/events_clean.csv
        data/processed/data_quality_summary.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "sample" / "sample_data.csv"
PROCESSED = ROOT / "data" / "processed"


def load_data(path: Path = RAW_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def clean_events(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    before_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())

    clean = df.drop_duplicates().copy()
    clean["event_time"] = pd.to_datetime(clean["event_time"], utc=True, errors="coerce")
    clean["price"] = pd.to_numeric(clean["price"], errors="coerce")
    clean = clean.dropna(subset=["event_time", "event_type", "user_id", "user_session", "product_id"])
    clean["price"] = clean["price"].fillna(0).clip(lower=0)

    clean["category_code"] = clean["category_code"].fillna("uncategorized")
    clean["brand"] = clean["brand"].fillna("unknown")
    clean["event_type"] = clean["event_type"].str.lower().str.strip()
    clean = clean[clean["event_type"].isin(["view", "cart", "purchase"])]

    clean["event_date"] = clean["event_time"].dt.date.astype(str)
    clean["event_hour"] = clean["event_time"].dt.hour
    clean["event_week"] = clean["event_time"].dt.tz_convert(None).dt.to_period("W-SUN").astype(str)
    clean["category_l1"] = clean["category_code"].str.split(".").str[0]
    clean["is_revenue_event"] = clean["event_type"].eq("purchase")
    clean["revenue"] = clean["price"].where(clean["is_revenue_event"], 0)

    quality = pd.DataFrame(
        [
            ("raw_rows", before_rows),
            ("duplicate_rows_removed", duplicate_rows),
            ("clean_rows", len(clean)),
            ("users", clean["user_id"].nunique()),
            ("sessions", clean["user_session"].nunique()),
            ("products", clean["product_id"].nunique()),
            ("missing_category_rows_filled", int(df["category_code"].isna().sum())),
            ("missing_brand_rows_filled", int(df["brand"].isna().sum())),
            ("min_event_time", clean["event_time"].min().isoformat()),
            ("max_event_time", clean["event_time"].max().isoformat()),
        ],
        columns=["metric", "value"],
    )
    return clean.sort_values("event_time"), quality


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    clean, quality = clean_events(load_data())
    clean.to_csv(PROCESSED / "events_clean.csv", index=False)
    quality.to_csv(PROCESSED / "data_quality_summary.csv", index=False)
    print(f"Wrote {len(clean):,} cleaned events to {PROCESSED / 'events_clean.csv'}")


if __name__ == "__main__":
    main()
