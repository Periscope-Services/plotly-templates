with
  cte as (
    select
      [created_at:aggregation] as ds
      , sum(price) as y
      , row_number() over(order by 1) as rownum
    from
      periscope_views.purchases
    group by
      1
  )
select
  ds
  , y as y$_revenue
  , case
    when rownum = 1
      then '[aggregation]'
    else null
  end as aggregation
from
  cte