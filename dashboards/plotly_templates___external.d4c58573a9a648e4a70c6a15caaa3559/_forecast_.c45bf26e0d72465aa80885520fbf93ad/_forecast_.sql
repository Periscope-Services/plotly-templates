/*****************************************
SQL output should have 3 columns:
   1) ds: the date or datetime

   2) y_value: the value to forecast. name it whatever makes sense, e.g. y_signups, y$_revenue, etc. add the dollar sign ($) to format in dollars.

   3) aggregation: the level of aggregation. can reference the [aggregation] filter. allowable values: hour, day, week, month, quarter, year
*****************************************/

select
  [created_at:aggregation] as ds
  , sum(price) as y$_revenue
  , '[aggregation]' as aggregation
from
  periscope_views.purchases
group by
  1