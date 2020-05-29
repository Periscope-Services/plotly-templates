select
  user_id
  , platform as s_platform
  , count(1) as y_purchases
from
  purchases
group by
  1
  , 2
having
  y_purchases > 0