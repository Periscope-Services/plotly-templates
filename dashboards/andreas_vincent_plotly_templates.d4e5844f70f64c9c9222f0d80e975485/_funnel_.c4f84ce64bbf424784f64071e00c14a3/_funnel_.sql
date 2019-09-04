with
  cte as (
    select
      'Signups' as phase
      , count(1) as value
    from
      periscope_views.users
    union all
    select
      'Plays' as phase
      , count(distinct user_id) as value
    from
      periscope_views.gameplays
    union all
    select
      'Purchases' as phase
      , count(distinct user_id) as value
    from
      periscope_views.purchases
  )
select
  *
from
  cte
order by
  2 desc