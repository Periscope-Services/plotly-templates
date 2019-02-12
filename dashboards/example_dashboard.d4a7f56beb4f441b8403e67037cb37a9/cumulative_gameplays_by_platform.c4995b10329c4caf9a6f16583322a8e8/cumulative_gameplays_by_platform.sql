select
  t.*
from
  (
    select
  -- apply built in aggregation filter to timestamp column - https://doc.periscopedata.com/article/aggregation-filter
      [created_at:aggregation] as created_date
      , count(*)
      , platform
    from
      periscope_views.gameplays
    group by
      1
      , 3
  )
  t
where
-- apply built in daterange filter to timestamp column - https://doc.periscopedata.com/article/date-range-filters
  [created_date=daterange]