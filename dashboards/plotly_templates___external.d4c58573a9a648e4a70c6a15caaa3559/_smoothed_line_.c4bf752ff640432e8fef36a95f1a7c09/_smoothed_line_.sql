select
  [created_at:week] as week
  , count(1)
from
  periscope_views.users
group by
  1
order by
  1