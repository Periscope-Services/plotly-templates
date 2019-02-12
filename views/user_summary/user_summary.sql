-- SQL Views are defined tables that can be saved and referenced in SQL queries. https://doc.periscopedata.com/article/views#content

-- Publish a view as a “Dataset” for exploratory usage by enabling the "Publish as Dataset" under "settings" on the right --->. 

--Users with the “Explorer” role can build charts using a visual interface. https://doc.periscopedata.com/article/creating-datasets

with
  CTE_purchase_summary as (
    select
      u.id as user_id
      , min([p.created_at:date]) as first_purchase_date
      , max([p.created_at:date]) as last_purchase_date
      , min(p.price) as min_purchase
      , max(p.price) as max_purchase
      , avg(p.price) as avg_purchase
      , count(distinct p.id) as num_purchases
      , sum(p.price) as total_purchases
    from
      periscope_views.users u
      left join periscope_views.purchases p on
        u.id = p.user_id
    group by
      u.id
  )
  , CTE_gameplay_summary as (
    select
      u.id as user_id
      ,min([g.created_at:date]) as first_gameplay_date
      , max([g.created_at:date]) as last_gameplay_date
      , count(distinct g.id) as num_gameplays
    from
      periscope_views.users u
      left join periscope_views.gameplays g on
        u.id = g.user_id
    group by
      u.id
  )
select
  u.id as user_id
  , u.platform
  , u.source
  , u.gender
  , u.latitude
  , u.longitude
  , [u.created_at:date] as signup_date
  , ps.first_purchase_date 
  , [ps.last_purchase_date:date] as last_purchase_date
  , coalesce(ps.min_purchase, 0) as min_purchase
  , coalesce(ps.max_purchase, 0) as max_purchase
  , coalesce(ps.avg_purchase, 0) as avg_purchase
  , ps.num_purchases
  , coalesce(ps.total_purchases, 0) as total_purchases
  , gs.first_gameplay_date 
  , [gs.last_gameplay_date:date] as last_gameplay_date
  , gs.num_gameplays
  , case
    when coalesce(ps.total_purchases, 0) >= 500
      then '500+_Platinum'
    when coalesce(ps.total_purchases, 0) > 250
      then '250+_Gold'
    when coalesce(ps.total_purchases, 0) > 100
      then '100+_Silver'
    when coalesce(ps.total_purchases, 0) > .99
      then 'premium'
    else 'free'
  end as user_mvp_level
  , coalesce([gs.last_gameplay_date:date] - [u.created_at:date] + 1, 0) as lifetime_days
from
  periscope_views.users u
  left join CTE_purchase_summary ps on
    u.id = ps.user_id
  left join CTE_gameplay_summary gs on
    u.id = gs.user_id