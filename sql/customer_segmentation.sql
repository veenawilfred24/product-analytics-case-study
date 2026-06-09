-- User segments based on observed behavior.

WITH user_metrics AS (
  SELECT
    user_id,
    COUNT(DISTINCT user_session) AS sessions,
    SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS carts,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases,
    SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue
  FROM events_clean
  GROUP BY user_id
)
SELECT
  *,
  CASE
    WHEN purchases > 0 THEN 'High-value users (purchasers)'
    WHEN carts > 0 THEN 'Cart abandoners'
    WHEN views > 0 THEN 'Browsers'
    ELSE 'Inactive users'
  END AS segment
FROM user_metrics;

