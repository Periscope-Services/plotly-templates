select
  platform as x_platform
  , sum(price) / 100000 as "current_$"
  , sum(price) * 1.5 / 100000 as "goal_$"
--   , 10 as current
--   , 15 as goal
from
  periscope_views.purchases
group by
  1