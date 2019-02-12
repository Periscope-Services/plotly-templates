-- ▲ Click the title to see how filter names name can be dynamically substituted.

with
  CTE_gameplays as (
    select
      --Use built in date formatter. https://doc.periscopedata.com/article/composing-sql-formatters
      [created_at:date] as date
      , platform
      , count(distinct user_id) as users
    from
      periscope_views.gameplays
    group by
      1
      , 2
  )
  , CTE_purchases as (
    select
      --Use built in date formatter. https://doc.periscopedata.com/article/composing-sql-formatters
      [created_at:date] as date
      , platform
      , sum(price) as spend
    from
      periscope_views.purchases
    group by
      1
      , 2
  )
select
  t.*
from
  (
    select
-- apply built in aggregation filter to timestamp column - https://doc.periscopedata.com/article/aggregation-filter
      [g.date:aggregation] as new_date
      --use built in currency formatter 
      , [coalesce(spend/users,0):$] revenue_per_user
      -- ^ Use built in currency formatter. https://doc.periscopedata.com/article/composing-sql-formatters
    from
      CTE_gameplays g
      left join CTE_purchases p on
        g.date = p.date
        and g.platform = p.platform
    where
      -- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
      [g.platform=Device]
  )
  t
where
--use built in daterange filter: https://doc.periscopedata.com/article/date-range-filters
  [new_date=daterange]