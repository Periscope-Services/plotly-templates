select
  [created_at:month] as date
  , sum(price) as revenue
from
  purchases
group by
  1