select
  [created_at:month] as date
  , sum(price) as "kpi_$"
from
  periscope_views.purchases
group by
  1
order by
  1