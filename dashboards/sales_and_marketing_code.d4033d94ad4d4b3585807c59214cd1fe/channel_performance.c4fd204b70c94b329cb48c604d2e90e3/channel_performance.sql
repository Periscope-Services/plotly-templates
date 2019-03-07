select
  channel
  , cost
  , leads
  , pipeline
  , dense_rank() over(order by cost desc, channel) as cost_rank
  , dense_rank() over(order by leads desc, channel) as leads_rank
  , dense_rank() over(order by pipeline desc, channel) as pipeline_rank
from
  table
order by
  2 desc
  , 3 desc
  , 4 desc
  , 1 asc
limit 20