--invoke Python for advanced analysis and access to additional plotting options through plotting libraries.

-- A frequent business question often posted is "What is the change in [users, units sold, views, etc]? Using Python's matplotlib library, one way to visualize this change is to visualize it alongside an arrow indicating the direction of change along with the context provided by the addition of the previous and current metric. Learn more @ https://community.periscopedata.com/t/80j9th/change-in-kpi-chart

with
  gameplay as (
    select
      [created_at:date] as date
      , count(distinct user_id) as users
    from
      periscope_views.gameplays
    where
      [platform=Device]
    group by
      1
  )
  , purchase as (
    select
      [created_at:date] as date
      , sum(price) as spend
    from
      periscope_views.purchases
    where
    -- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters

-- See this doc to learn how to add a filter to the dashboard: https://doc.periscopedata.com/article/add-remove-filters
      [platform=Device]
    group by
      1
  )
select
  round(coalesce(spend/users,0),2) revenue_per_user
from
  gameplay g
  left join purchase p on
    g.date = p.date
where
  g.date = [getdate():date] - interval '7 day'
union all
select
  round(coalesce(spend/users,0),2) revenue_per_user
from
  gameplay g
  left join purchase p on
    g.date = p.date
where
  g.date = [getdate():date]