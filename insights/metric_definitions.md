# Metric Definitions

## Business Objective

Improve e-commerce conversion by identifying where users lose momentum between product views, cart activity, and purchase. The dataset contains 49,985 cleaned events from 10,537 users and 12,436 sessions during a 2 hour 48 minute sample window on 2019-11-01.

## North Star Metric

**Purchase Conversion Rate**

Definition: users with an observed purchase divided by users with an observed product view.

Measured result from this dataset:

- Ordered view-to-purchase conversion: **1.37%** of viewed users reached purchase after a cart event.
- Raw purchaser share: **4.36%** of all users purchased at least once during the sample window.

Purchase Conversion Rate is the best North Star for this project because the product problem is not traffic generation; it is turning existing shopping intent into completed orders.

## Supporting Metrics

**View-to-Cart Rate**

- Definition: users who cart after a view divided by users who view.
- Measured result: **2.82%**.
- Why it matters: this is the clearest signal of product discovery and product detail page strength. Low view-to-cart means users are browsing but not finding enough value, confidence, or urgency to start checkout.

**Cart-to-Purchase Rate**

- Definition: users who purchase after cart divided by users who cart after view.
- Measured result: **48.48%**.
- Why it matters: this isolates checkout and purchase-completion quality among users who already showed intent.

**Drop-Off Rate**

- Definition: one minus stage-to-stage conversion.
- Measured result: **97.18%** drop from view to cart and **51.52%** drop from cart to purchase.
- Why it matters: it helps Product decide whether the bigger issue is product discovery, pricing/offer clarity, or checkout friction.

**Same-Window Repeat Session Rate**

- Definition: users with more than one session in the available sample window divided by all users.
- Measured result: **12.33%**.
- Why it matters: the dataset covers less than one day, so Day 1 and Day 7 retention cannot be observed. Same-window repeat activity is the best available proxy for short-term return intent.

**Category Conversion Rate**

- Definition: ordered view-to-purchase conversion by top-level category.
- Measured result: Electronics converts at **2.67%**, above the overall ordered conversion rate of **1.37%**.
- Why it matters: category-level conversion identifies where merchandising and product experience are already working and where traffic is not turning into demand.

## Guardrail Metrics

**Revenue per Purchaser**

- Definition: purchase revenue divided by purchasing users.
- Measured result: $164,058.23 revenue across 459 purchasers, or roughly **$357.42 per purchaser**.
- Why it matters: conversion improvements should not come from discounting or lower-quality purchases alone.

**Cart Abandoner Share**

- Definition: users with cart events and no purchases divided by all users.
- Measured result: **1.47%**.
- Why it matters: this group has the clearest unfinished purchase intent and should be tracked when checkout changes ship.

**Data Coverage**

- Definition: duration and completeness of the behavioral window.
- Measured result: one short window from 00:00:00 to 02:48:26 UTC on 2019-11-01.
- Why it matters: retention and experiment decisions should be treated as directional until longer observation windows are available.

