select
  t.*
from
  (
    select
    -- apply built in aggregation filter to timestamp column - https://doc.periscopedata.com/article/aggregation-filter
      [g.created_at:aggregation] as created_date
      , g.platform
      , count(distinct u.id)
    from
      periscope_views.gameplays g
      join periscope_views.users u on
        g.user_id = u.id
    group by
      1
      , 2
  )
  t
where
--use built in daterange filter: https://doc.periscopedata.com/article/date-range-filters
  [created_date=daterange]