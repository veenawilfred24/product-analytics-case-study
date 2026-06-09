-- Ordered funnel: view -> cart -> purchase.
-- Assumes a cleaned events table with:
-- user_id, event_time, event_type, category_l1, event_hour

WITH first_view AS (
  SELECT user_id, MIN(event_time) AS view_time
  FROM events_clean
  WHERE event_type = 'view'
  GROUP BY user_id
),
first_cart_after_view AS (
  SELECT e.user_id, MIN(e.event_time) AS cart_time
  FROM events_clean e
  JOIN first_view v ON e.user_id = v.user_id
  WHERE e.event_type = 'cart'
    AND e.event_time >= v.view_time
  GROUP BY e.user_id
),
first_purchase_after_cart AS (
  SELECT e.user_id, MIN(e.event_time) AS purchase_time
  FROM events_clean e
  JOIN first_cart_after_view c ON e.user_id = c.user_id
  WHERE e.event_type = 'purchase'
    AND e.event_time >= c.cart_time
  GROUP BY e.user_id
),
funnel_flags AS (
  SELECT
    v.user_id,
    1 AS viewed,
    CASE WHEN c.user_id IS NOT NULL THEN 1 ELSE 0 END AS carted,
    CASE WHEN p.user_id IS NOT NULL THEN 1 ELSE 0 END AS purchased
  FROM first_view v
  LEFT JOIN first_cart_after_view c USING (user_id)
  LEFT JOIN first_purchase_after_cart p USING (user_id)
)
SELECT
  SUM(viewed) AS view_users,
  SUM(carted) AS cart_users,
  SUM(purchased) AS purchase_users,
  SUM(carted) * 1.0 / SUM(viewed) AS view_to_cart_rate,
  SUM(purchased) * 1.0 / NULLIF(SUM(carted), 0) AS cart_to_purchase_rate,
  SUM(purchased) * 1.0 / SUM(viewed) AS view_to_purchase_rate
FROM funnel_flags;

