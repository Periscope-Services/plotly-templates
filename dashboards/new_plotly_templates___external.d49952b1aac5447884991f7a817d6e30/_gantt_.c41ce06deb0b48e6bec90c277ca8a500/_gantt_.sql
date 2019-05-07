select
  platform as task
  , min(created_at) as start
  , max(created_at) as finish
from
  periscope_views.gameplays
group by
  1
order by
  2 desc

select 1