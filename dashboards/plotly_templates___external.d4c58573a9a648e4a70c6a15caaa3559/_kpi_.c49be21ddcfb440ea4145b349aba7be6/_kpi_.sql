select
  [created_at:month] as date
  , sum(price) as revenue
from
  periscope_views.purchases
group by
  1