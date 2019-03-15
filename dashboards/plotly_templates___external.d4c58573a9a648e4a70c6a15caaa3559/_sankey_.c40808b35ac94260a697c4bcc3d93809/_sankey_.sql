with
  u as (
    select
      id
    from
      periscope_views.users
    where
      source is not null
      and platform is not null
      and id % 1000 = 29
  )
select
  u.id as unique_id
  , source as stage_name
  , dateadd(day, -100, created_at) as sort
from
  u
  inner join periscope_views.users on
    u.id = users.id
union all
select
  u.id
  , platform
  , created_at
from
  u
  inner join periscope_views.users on
    u.id = users.id
union all
select
  u.id
  , 'Made a purchase'
  , dateadd(day, 100, min(created_at))
from
  u
  inner join periscope_views.purchases on
    u.id = purchases.user_id
group by
  1
  , 2