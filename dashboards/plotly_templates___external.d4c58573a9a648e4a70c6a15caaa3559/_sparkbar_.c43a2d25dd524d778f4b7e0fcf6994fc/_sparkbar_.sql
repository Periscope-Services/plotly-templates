select
  [created_at:month] as ds_month
  , sum(price) as "y$_revenue"
from
  purchases
-- where
--   [created_at:month] >= dateadd(month, -5, getdate())
group by
  1
order by
  1 desc
limit 4