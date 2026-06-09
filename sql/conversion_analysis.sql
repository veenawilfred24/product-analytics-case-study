-- Conversion by product category and hour.

SELECT
  category_l1,
  event_hour,
  COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS view_users,
  COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS cart_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchase_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) * 1.0
    / NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END), 0) AS raw_view_to_purchase_rate,
  SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue
FROM events_clean
GROUP BY category_l1, event_hour
ORDER BY revenue DESC;

