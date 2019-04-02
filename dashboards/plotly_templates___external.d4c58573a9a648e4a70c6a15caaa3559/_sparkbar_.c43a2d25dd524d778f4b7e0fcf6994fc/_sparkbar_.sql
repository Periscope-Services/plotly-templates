select
  [created_at:month] as ds_month
  , sum(price) as "y$_revenue"
from
  periscope_views.purchases
where 1=1
--   [created_at:month] >= dateadd(month, -5, getdate())
group by
  1
order by
  1