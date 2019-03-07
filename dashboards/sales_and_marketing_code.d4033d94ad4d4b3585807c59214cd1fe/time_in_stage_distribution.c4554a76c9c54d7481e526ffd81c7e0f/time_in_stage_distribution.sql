select
  stage_name
  , stage_begin
  , stage_end
  , datediff(day, stage_begin, stage_end) as difference
from
  table
order by
  2 desc