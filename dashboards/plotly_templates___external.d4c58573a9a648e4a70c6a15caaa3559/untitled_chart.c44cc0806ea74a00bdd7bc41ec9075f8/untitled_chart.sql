select
  platform as x_platform
  , sum(price) as "current_$"
  , sum(price) * 1.5 as "goal_$"
from
  periscope_views.purchases
group by
  1