select
  platform as task
  , min(created_at) as start
  , max(created_at) as finish
from
  gameplays
group by
  1
order by
  2 desc