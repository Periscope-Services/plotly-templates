/*****************************************
SQL output should have 2 columns:
   1) ds_aggregation: the date or datetime. name should be ds_hour, ds_day, ds_week, ds_month, ds_quarter, or ds_year. if you are using Periscope's aggregation filter, you can name it ds_[aggregation]

   2) y_value: the value to forecast. name it whatever makes sense, e.g. y_signups, y$_revenue, etc. add the dollar sign ($) to format in dollars.
*****************************************/

select
  [created_at:aggregation] as ds_[aggregation]
  , sum(price) as y$_revenue
from
  periscope_views.purchases
group by
  1