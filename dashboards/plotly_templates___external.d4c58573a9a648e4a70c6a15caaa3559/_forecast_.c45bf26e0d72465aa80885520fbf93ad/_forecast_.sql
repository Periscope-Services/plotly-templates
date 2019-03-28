select
  [created_at:aggregation] as ds
  , sum(price) as y$_revenue
  , '[aggregation]' as aggregation
from
  periscope_views.purchases
group by
  1