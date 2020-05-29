select
  platform as x_platform
  , sum(price) as "current_$"
  , sum(price) * 1.5 as "goal_$"
from
  purchases
where
  [created_at=7days]
group by
  1
order by
  3
  , 2