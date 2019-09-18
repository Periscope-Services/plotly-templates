select
  [created_at:month]
  , count(1)
from
  periscope_views.gameplays
group by
  1