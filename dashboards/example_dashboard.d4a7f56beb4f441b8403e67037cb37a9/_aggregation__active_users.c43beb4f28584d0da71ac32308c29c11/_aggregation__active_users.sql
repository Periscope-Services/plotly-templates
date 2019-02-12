-- ▲ Click the title to see how filter names name can be dynamically substituted.

select
  t.*
from
  (
    select
    -- apply built in aggregation filter to timestamp column - https://doc.periscopedata.com/article/aggregation-filter
      [gameplays.created_at:aggregation] as created_date
      , gameplays.platform
      , count(distinct users.id)
    from
      periscope_views.gameplays
      join periscope_views.users on
        gameplays.user_id = users.id
    group by
      1
      , 2
  )
  t
where
--use built in daterange filter: https://doc.periscopedata.com/article/date-range-filters
  [created_date=daterange]