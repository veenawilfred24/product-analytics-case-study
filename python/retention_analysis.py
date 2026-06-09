"""Retention cohorts from first interaction date.

The provided sample covers less than one calendar day, so Day 1 and Day 7
retention are not observable. The script still writes the requested cohort
tables and adds same-window repeat-session retention as the actionable proxy.
"""

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


def build_retention(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    user_dates = (
        df.groupby("user_id")
        .agg(first_interaction=("event_time", "min"), last_interaction=("event_time", "max"), sessions=("user_session", "nunique"))
        .reset_index()
    )
    user_dates["cohort_date"] = user_dates["first_interaction"].dt.date.astype(str)
    user_dates["cohort_week"] = user_dates["first_interaction"].dt.tz_convert(None).dt.to_period("W-SUN").astype(str)
    user_dates["day_1_retained"] = user_dates["last_interaction"].dt.date > user_dates["first_interaction"].dt.date
    user_dates["day_7_retained"] = user_dates["last_interaction"] >= user_dates["first_interaction"] + pd.Timedelta(days=7)
    user_dates["same_window_repeat_session"] = user_dates["sessions"] > 1
    user_dates["active_30m_later"] = user_dates["last_interaction"] >= user_dates["first_interaction"] + pd.Timedelta(minutes=30)

    daily = (
        user_dates.groupby("cohort_date")
        .agg(
            cohort_users=("user_id", "nunique"),
            day_1_retained_users=("day_1_retained", "sum"),
            day_7_retained_users=("day_7_retained", "sum"),
            repeat_session_users=("same_window_repeat_session", "sum"),
            active_30m_later_users=("active_30m_later", "sum"),
        )
        .reset_index()
    )
    daily["day_1_retention"] = daily["day_1_retained_users"] / daily["cohort_users"]
    daily["day_7_retention"] = daily["day_7_retained_users"] / daily["cohort_users"]
    daily["same_window_repeat_session_rate"] = daily["repeat_session_users"] / daily["cohort_users"]
    daily["active_30m_later_rate"] = daily["active_30m_later_users"] / daily["cohort_users"]

    weekly = (
        user_dates.groupby("cohort_week")
        .agg(
            cohort_users=("user_id", "nunique"),
            repeat_session_users=("same_window_repeat_session", "sum"),
            day_1_retained_users=("day_1_retained", "sum"),
            day_7_retained_users=("day_7_retained", "sum"),
        )
        .reset_index()
    )
    weekly["week_level_observed_retention"] = weekly["repeat_session_users"] / weekly["cohort_users"]
    weekly["day_1_retention"] = weekly["day_1_retained_users"] / weekly["cohort_users"]
    weekly["day_7_retention"] = weekly["day_7_retained_users"] / weekly["cohort_users"]
    return daily, weekly


def main() -> None:
    daily, weekly = build_retention(load_events())
    daily.to_csv(PROCESSED / "retention_daily_cohorts.csv", index=False)
    weekly.to_csv(PROCESSED / "retention_weekly_cohorts.csv", index=False)
    print("Wrote retention cohort outputs.")


if __name__ == "__main__":
    main()
