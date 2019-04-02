select
  [created_at:month] as ds_month
  , sum(price) as "y$_revenue"
from
  periscope_views.purchases
group by
  1