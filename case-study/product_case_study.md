# Improving User Growth and Retention Using Product Analytics

## 1. Executive Summary

The dataset reveals a classic e-commerce activation problem. Users are arriving and viewing products, but very few are progressing to cart. After cleaning 49,985 events, the ordered funnel shows 10,535 viewed users, 297 users who carted after viewing, and 144 users who purchased after carting.

The largest drop-off occurs between view and cart: **97.18%** of users fail to translate product views into purchase intent. In contrast, cart-to-purchase conversion is relatively strong at **48.48%**, indicating that once users demonstrate intent, they are likely to complete the transaction.

The key insight is that conversion failure occurs before intent formation, not during checkout, making early funnel optimization the highest-leverage growth opportunity.

## 2. Business Problem

The product team needs to understand why e-commerce traffic is not converting into purchases. The key decision is where to invest first:

- Product discovery and product detail pages
- Cart and checkout completion
- Category merchandising
- Retention and lifecycle programs
- Experimentation around onboarding or shopping guidance

This analysis focuses on identifying the primary constraint in the user journey and recommending the highest-impact product actions.

## 3. Dataset

Source file: `data/sample/sample_data.csv`

Cleaned output: `data/processed/events_clean.csv`

The dataset contains event-level behavior with product views, cart events, purchases, product/category fields, brand, price, user ID, and session ID.

Cleaning summary:

- Raw rows: **49,999**
- Duplicate rows removed: **14**
- Clean rows: **49,985**
- Users: **10,537**
- Sessions: **12,436**
- Products: **13,570**
- Missing category rows filled as `uncategorized`: **17,028**
- Missing brand rows filled as `unknown`: **8,099**
- Event window: **2019-11-01 00:00:00 UTC to 2019-11-01 02:48:26 UTC**

Device is not available in the dataset, so device segmentation is not included.

## 4. Metrics

The North Star Metric is **Purchase Conversion Rate**, defined as the share of viewed users who complete the ordered journey to purchase.

Measured result:

- Ordered view-to-purchase conversion: **1.37%**
- Raw purchaser share: **4.36%**

Supporting metrics:

- View-to-cart rate: **2.82%**
- Cart-to-purchase rate: **48.48%**
- Same-window repeat-session rate: **12.33%**
- Category-level conversion
- Revenue per purchaser: approximately **$357.42**

These metrics help identify whether the primary constraint lies in product activation, checkout efficiency, retention, or merchandising quality.

## 5. Funnel Analysis

The ordered funnel is:

View -> Cart -> Purchase

Results:

- Viewed users: **10,535**
- Cart users after view: **297**
- Purchase users after cart: **144**
- View-to-cart rate: **2.82%**
- Cart-to-purchase rate: **48.48%**
- View-to-purchase rate: **1.37%**

The magnitude of the drop-off indicates that users are not failing at checkout — they are failing to form purchase intent in the first place. This reframes the problem from checkout optimization to product discovery and value communication.

Category results strengthen that interpretation. Electronics is the standout category, with **2.67%** ordered view-to-purchase conversion and **$121,229.39** in revenue. Uncategorized products have **4,254 viewed users** but only **0.33%** ordered conversion, which makes taxonomy quality a product analytics issue and a merchandising issue.

## 6. Retention Analysis

The requested Day 1 and Day 7 retention cohorts were created, but the dataset only covers one short window on one date. As a result:

- Day 1 retention: **0.00%**
- Day 7 retention: **0.00%**
- Same-window repeat-session rate: **12.33%**
- Active 30 minutes later: **3.94%**

The honest product conclusion is that long-term retention cannot be evaluated from this extract. The available signal says some users do return within the same short window, but lifecycle decisions need a longer multi-day dataset.
Any attempt to derive lifecycle insights would risk overfitting to incomplete behavioral signals.

## 7. Segmentation

Users were segmented into mutually exclusive behavior groups:

- **Browsers:** 9,923 users, **94.17%** of users. They viewed products but did not cart or purchase.
- **High-value users (purchasers):** 459 users, **4.36%** of users, generating **$164,058.23** in purchase revenue.
- **Cart abandoners:** 155 users, **1.47%** of users. They carted but did not purchase.
- **Inactive users:** none observed because every user in the dataset has at least one event.

The distribution shows that growth depends more on activating browsers than optimizing already engaged users, as the largest population sits at the top of the funnel.

Business actions:

- Browsers need product discovery and PDP improvements.
- Cart abandoners need checkout recovery and friction diagnosis.
- Purchasers need value protection, repeat-purchase paths, and revenue guardrails.

## 8. A/B Test

Because the dataset has no experiment, the analysis simulates random assignment only. Outcomes are not simulated; conversion comes from observed purchase behavior.

Experiment setup:

- Variant A: current experience
- Variant B: proposed improved shopping/onboarding experience
- Metric: user purchase conversion
- Test: two-proportion z-test
- Assignment seed: 42

Results:

- Variant A: 5,284 users, 225 converted, **4.26%** conversion
- Variant B: 5,253 users, 234 converted, **4.45%** conversion
- Absolute lift: **0.20 percentage points**
- Relative lift: **4.61%**
- P-value: **0.621**

The lack of statistical significance reinforces the importance of disciplined experimentation; product changes should not be shipped based on directional improvements alone.

Decision: **Do not ship based on this result.** The observed difference is not statistically significant and should be treated as noise. A real experiment should run over a longer window with pre-registered sample size and guardrails for revenue per purchaser and cart-to-purchase conversion.

## 9. Key Insights

1. Product view-to-cart is the largest measured bottleneck.
2. Checkout completion is meaningful but secondary to product activation.
3. Electronics is the strongest category and should be used as the merchandising benchmark.
4. Uncategorized traffic is too large and too weakly converting to leave unresolved.
5. Most users are browsers only, so activation matters more than cart recovery alone.
6. Cart abandoners are small but highly actionable.
7. Retention cannot be judged from a less-than-one-day extract.
8. The A/B simulation does not provide evidence to ship Variant B.

## 10. Final Recommendation

The highest-impact product decision is to improve view-to-cart conversion before investing in checkout optimization or acquisition. Start with electronics as the positive benchmark and uncategorized products as the cleanup priority. Improve category taxonomy, product detail page clarity, delivery/returns confidence, recommendations, and cart calls to action.

In parallel, build a cart abandoner recovery path, but do not let checkout work distract from the larger activation gap. For retention and experimentation, request a longer event window before making roadmap-level decisions.

