with
  u as (
    select
      id
    from
      users
    where
      source is not null
      and platform is not null
      and id % 1000 = 29
  )
select
  u.id as unique_id
  , source as stage_name
  , 1 as sort
from
  u
  inner join users on
    u.id = users.id
union all
select
  u.id
  , platform
  , 2
from
  u
  inner join users on
    u.id = users.id
union all
select
  u.id
  , case
    when random() > .4
      then 'Made a purchase'
    else 'No purchase'
  end
  , 3
from
  u