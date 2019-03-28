with
  cte as (
    select
      [created_at:aggregation] as ds
      , count(1) as y
      , row_number() over(order by 1) as rownum
    from
      periscope_views.users
    group by
      1
  )
select
  ds
  , y as y_signups
  , case
    when rownum = 1
      then '[aggregation]'
    else null
  end as aggregation
from
  cte