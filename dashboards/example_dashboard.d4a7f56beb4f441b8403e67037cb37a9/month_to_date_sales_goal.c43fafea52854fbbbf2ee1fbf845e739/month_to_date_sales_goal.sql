--invoke Python for advanced analysis and access to additional plotting options through plotting libraries.

-- "How Close are we to our goal?" Radial Bar Charts are great at conveying progress vs goal in an easily digestible fashion. Learn More @ https://community.periscopedata.com/t/36gsvm/chart-type-radial-bar-chart-in-matplotlib-python

with
  goals as (
    select
      'android' as platform
      , 1200000 as goal
    union all
    select
      'iOS'
      , 2000000
    union all
    select
      'web'
      , 1000000
  )
  , mtd_sales as (
    select
      platform
      , sum(price) as revenue
    from
      periscope_views.purchases
    where
    
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters

-- See this doc to learn how to add a filter to the dashboard: https://doc.periscopedata.com/article/add-remove-filters
      [purchases.platform=Device]
      and [purchases.created_at:month] = [getdate():month]
    group by
      1
  )
select
  sum(revenue) as revenue
  , sum(goal) as goal
from
  mtd_sales
  join goals on
    mtd_sales.platform = goals.platform