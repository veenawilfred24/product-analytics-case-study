"""Generate dashboard preview images from processed analysis tables."""

from __future__ import annotations

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))

import matplotlib.pyplot as plt
import pandas as pd


PROCESSED = ROOT / "data" / "processed"
ASSETS = ROOT / "dashboard" / "assets"


COLORS = {
    "teal": "#2f6f73",
    "gold": "#d89d42",
    "purple": "#7b6d8d",
    "red": "#c84c3d",
    "green": "#4f8a5b",
    "gray": "#59656f",
}


def pct(value: float) -> str:
    return f"{value:.1%}"


def finish(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)


def funnel_chart() -> None:
    df = pd.read_csv(PROCESSED / "funnel_summary.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["stage"], df["users"], color=[COLORS["teal"], COLORS["gold"], COLORS["red"]])
    for i, row in df.iterrows():
        ax.text(i, row["users"] + 180, f"{int(row['users']):,}", ha="center", fontweight="bold")
        if row["stage"] != "view":
            ax.text(i, row["users"] + 620, pct(row["overall_conversion_rate"]), ha="center", fontsize=10)
    ax.set_title("Ordered Funnel: View -> Cart -> Purchase", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("Users")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ASSETS / "funnel_chart.png")


def retention_curve() -> None:
    df = pd.read_csv(PROCESSED / "retention_daily_cohorts.csv").iloc[0]
    labels = ["Same-window repeat", "Active 30m later", "Day 1", "Day 7"]
    values = [
        df["same_window_repeat_session_rate"],
        df["active_30m_later_rate"],
        df["day_1_retention"],
        df["day_7_retention"],
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(labels, values, marker="o", linewidth=3, color=COLORS["teal"])
    for i, value in enumerate(values):
        ax.text(i, value + 0.006, pct(value), ha="center", fontweight="bold")
    ax.set_ylim(0, max(values) + 0.05)
    ax.set_title("Retention Signals From Available Window", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("Retention rate")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    finish(fig, ASSETS / "retention_curve.png")


def segment_distribution() -> None:
    df = pd.read_csv(PROCESSED / "segment_summary.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [COLORS["gray"], COLORS["teal"], COLORS["gold"]]
    ax.barh(df["segment"], df["users"], color=colors[: len(df)])
    for i, row in df.iterrows():
        ax.text(row["users"] + 90, i, f"{int(row['users']):,} ({row['user_share']:.1%})", va="center", fontweight="bold")
    ax.set_title("User Segment Distribution", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("Users")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ASSETS / "segment_distribution.png")


def category_conversion() -> None:
    df = pd.read_csv(PROCESSED / "funnel_by_category.csv").head(8).sort_values("view_to_purchase_rate").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(df["category_l1"], df["view_to_purchase_rate"], color=COLORS["teal"])
    for i, row in df.iterrows():
        ax.text(row["view_to_purchase_rate"] + 0.001, i, pct(row["view_to_purchase_rate"]), va="center", fontweight="bold")
    ax.set_title("Ordered Conversion by Category", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("View-to-purchase rate")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ASSETS / "conversion_by_category.png")


def ab_test_results() -> None:
    variants = pd.read_csv(PROCESSED / "ab_test_variant_summary.csv")
    test = pd.read_csv(PROCESSED / "ab_test_results.csv").set_index("metric")["value"].to_dict()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(variants["variant"], variants["conversion_rate"], color=[COLORS["gray"], COLORS["teal"]])
    for i, row in variants.iterrows():
        ax.text(i, row["conversion_rate"] + 0.001, pct(row["conversion_rate"]), ha="center", fontweight="bold")
    ax.set_title(f"A/B Simulation: Conversion Rate by Variant (p={float(test['p_value']):.3f})", loc="left", fontsize=14, fontweight="bold")
    ax.set_ylabel("Purchase conversion rate")
    ax.set_ylim(0, variants["conversion_rate"].max() + 0.02)
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ASSETS / "ab_test_results.png")


def executive_overview() -> None:
    funnel = pd.read_csv(PROCESSED / "funnel_summary.csv").set_index("stage")
    retention = pd.read_csv(PROCESSED / "retention_daily_cohorts.csv").iloc[0]
    segments = pd.read_csv(PROCESSED / "segment_summary.csv")
    metrics = [
        ("View-to-cart", funnel.loc["cart", "overall_conversion_rate"]),
        ("View-to-purchase", funnel.loc["purchase", "overall_conversion_rate"]),
        ("Repeat-session", retention["same_window_repeat_session_rate"]),
        ("Purchaser share", segments.loc[segments["segment"].str.contains("purchasers"), "user_share"].iloc[0]),
    ]
    fig, ax = plt.subplots(figsize=(10, 5))
    labels, values = zip(*metrics)
    ax.bar(labels, values, color=[COLORS["teal"], COLORS["red"], COLORS["gold"], COLORS["purple"]])
    for i, value in enumerate(values):
        ax.text(i, value + 0.005, pct(value), ha="center", fontweight="bold")
    ax.set_title("Executive KPI Snapshot", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("Rate")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, ASSETS / "executive_overview.png")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    executive_overview()
    funnel_chart()
    retention_curve()
    segment_distribution()
    category_conversion()
    ab_test_results()
    print(f"Wrote dashboard assets to {ASSETS}")


if __name__ == "__main__":
    main()
