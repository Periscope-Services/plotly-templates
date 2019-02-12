-- PERISCOPE_DRAG_DROP_QUERY
SELECT user_summary.source as "source", COUNT(DISTINCT user_summary.user_id) as "user_id"
 FROM [user_summary]
 GROUP BY user_summary.source -- GROUP_BY_FIELD
 GROUP BY 1 -- GROUP_BY_INDEX