-- A/B readout template after users have been assigned to variants.
-- Assignment can be simulated for analysis practice, but outcomes should come
-- from observed purchase behavior.

SELECT
  variant,
  COUNT(DISTINCT user_id) AS users,
  COUNT(DISTINCT CASE WHEN converted THEN user_id END) AS converted_users,
  COUNT(DISTINCT CASE WHEN converted THEN user_id END) * 1.0 / COUNT(DISTINCT user_id) AS conversion_rate
FROM ab_assignments
GROUP BY variant
ORDER BY variant;

