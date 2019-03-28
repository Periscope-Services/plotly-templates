/*****************************************
SQL output should have 3 columns:
   1) ds: the date or datetime

   2) y_value: the value to forecast. name it whatever makes sense, e.g. y_signups, y$_revenue, etc. add the dollar sign ($) to format in dollars.

   3) aggregation: the level of date aggregation. can reference the [aggregation] filter. allowable values: hour, day, week, month, quarter, year

   4) in_progress: true if the value is for the current period, false if it's a prior period
*****************************************/

select
  [created_at:aggregation] as ds
  , sum(price) as y$_revenue
  , '[aggregation]' as aggregation
  , [created_at:aggregation] = [getdate():pst:aggregation] as in_progress
from
  periscope_views.purchases
group by
  1