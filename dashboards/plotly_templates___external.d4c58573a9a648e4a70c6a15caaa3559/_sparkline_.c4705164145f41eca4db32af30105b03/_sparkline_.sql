select
  [created_at:month] as date
  , sum(price) as "kpi_$"
from
  purchases
group by
  1
order by
  1