-- Cohort retention from first interaction date.
-- The provided sample covers less than one day; Day 1 and Day 7 retention
-- are included for completeness and will be zero unless more days are added.

WITH user_activity AS (
  SELECT
    user_id,
    MIN(event_time) AS first_interaction,
    MAX(event_time) AS last_interaction,
    COUNT(DISTINCT user_session) AS sessions
  FROM events_clean
  GROUP BY user_id
)
SELECT
  DATE(first_interaction) AS cohort_date,
  COUNT(*) AS cohort_users,
  SUM(CASE WHEN DATE(last_interaction) > DATE(first_interaction) THEN 1 ELSE 0 END) AS day_1_retained_users,
  SUM(CASE WHEN last_interaction >= first_interaction + INTERVAL '7 day' THEN 1 ELSE 0 END) AS day_7_retained_users,
  SUM(CASE WHEN sessions > 1 THEN 1 ELSE 0 END) AS same_window_repeat_session_users,
  SUM(CASE WHEN sessions > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS same_window_repeat_session_rate
FROM user_activity
GROUP BY 1
ORDER BY 1;

