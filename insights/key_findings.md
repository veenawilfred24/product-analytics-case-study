# Key Findings

## 1. Product Views Are Not Translating Into Cart Intent

**Observation:** 10,535 users viewed products, but only 297 users added to cart after a view.

**Comparison:** The ordered view-to-cart rate is **2.82%**, meaning **97.18%** of viewed users drop before cart.

**Implication:** This indicates users are not failing at checkout — they are failing to form purchase intent after viewing products, making this the primary constraint in the funnel.

**Recommended action:** Prioritize product detail page improvements: clearer price/value messaging, stronger product imagery, delivery/returns clarity, and better related-product recommendations.

## 2. Checkout Performs Better Than Product Discovery, But Still Leaks Intent

**Observation:** 144 of 297 ordered cart users completed a purchase.

**Comparison:** Cart-to-purchase conversion is **48.48%**, far stronger than view-to-cart but still leaving **51.52%** of carting users unconverted.

**Implication:** Users who cart demonstrate strong purchase intent, but the checkout experience still fails to convert roughly half of qualified users.

**Recommended action:** Improve cart persistence, shipping-cost visibility, payment trust signals, and checkout error tracking.

## 3. Electronics Is Carrying the Business

**Observation:** Electronics generated **119 ordered purchases** and **$121,229.39** in purchase revenue.

**Comparison:** Electronics converts at **2.67%** from view to purchase, almost double the overall ordered conversion rate of **1.37%**.

**Implication:** Electronics has the strongest combination of demand, conversion, and revenue quality in the observed data.

**Recommended action:** Use electronics as the benchmark category: audit its PDP structure, pricing, brand mix, and merchandising patterns, then apply the winning patterns to weaker categories.

This suggests that category-level experience, pricing, or product mix in electronics is closer to an optimal state than other categories.

## 4. Uncategorized Traffic Is Too Large To Ignore

**Observation:** 17,028 raw rows were missing `category_code` and were classified as `uncategorized`.

**Comparison:** Uncategorized users produced 4,254 viewed users but only a **0.33%** ordered view-to-purchase rate.

**Implication:** Missing category taxonomy creates both a data quality issue and a product discovery issue, limiting the team’s ability to optimize a significant portion of user behavior.

**Recommended action:** Fix category instrumentation and taxonomy mapping before making major merchandising decisions for uncategorized products.

## 5. Most Users Are Browsers Only

**Observation:** 9,923 of 10,537 users are browsers with views but no cart or purchase.

**Comparison:** Browsers represent **94.17%** of users, while purchasers represent **4.36%** and cart abandoners represent **1.47%**.

**Implication:** Growth depends more on activating passive browsers than optimizing already engaged users, as the largest user segment sits at the top of the funnel.

**Recommended action:** Build a browser activation plan: recently viewed modules, category landing-page improvements, price confidence cues, and stronger calls to action.

## 6. Cart Abandoners Are Small But Highly Actionable

**Observation:** 155 users added to cart but did not purchase.

**Comparison:** This group is much smaller than the browser segment, but they have stronger purchase intent because they crossed the cart threshold.

**Implication:** Cart abandoners represent a high-intent segment that requires targeted intervention rather than general product improvements.

**Recommended action:** Trigger cart recovery journeys, saved cart reminders, and checkout friction surveys for this segment.

## 7. Retention Cannot Be Judged From This Sample Alone

**Observation:** The dataset spans only 2 hours and 48 minutes on one date.

**Comparison:** Day 1 and Day 7 retention are both **0.00%** because the observation window does not include later days; same-window repeat-session rate is **12.33%**.

**Implication:** Long-term retention conclusions would be overclaimed from this file. Any attempt to optimize retention from this dataset would risk overfitting to incomplete behavioral signals.

**Recommended action:** Use same-window repeat behavior as a short-term signal, but require a multi-day extract before making lifecycle or retention roadmap decisions.

## 8. The A/B Simulation Does Not Support Shipping Variant B

**Observation:** Simulated random assignment produced a **4.26%** conversion rate for Variant A and **4.45%** for Variant B using observed purchase outcomes.

**Comparison:** Variant B is up **0.20 percentage points**, but the p-value is **0.621**, which is not statistically significant.

**Implication:** The observed lift is indistinguishable from random variation, indicating no reliable evidence that Variant B improves conversion. This highlights the importance of disciplined experimentation — product decisions should not be based on directional improvements alone.

**Recommended action:** Do not ship based on this simulation. Run a real experiment with pre-registered sample size, longer exposure, and guardrails for revenue per purchaser and cart-to-purchase conversion.

