with
  CTE_ad as (
    select
      network
      , sum(spend) as spend
    from
      periscope_views.ad_spend
    group by
      network
  )
  , CTE_install as (
    select
      source
      , count(distinct user_id) as users
      , sum(total_purchases) as revenue
    from 
    -- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
      [user_summary]
    where
    -- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
      [user_mvp_level=MVP_Level]
    group by
      source
  )
select
  coalesce(network, source) as source
  , [coalesce(spend,0):$] as spend
  -- ^ Use built in currency formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
  , users
  , [spend/users:$] as cost_per_install
  -- ^ Use built in currency formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
  , [revenue/users:$] as avg_revenue_per_user
  -- ^ Use built in currency formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
from
  CTE_ad a
  full join CTE_install i on
    a.network = i.source