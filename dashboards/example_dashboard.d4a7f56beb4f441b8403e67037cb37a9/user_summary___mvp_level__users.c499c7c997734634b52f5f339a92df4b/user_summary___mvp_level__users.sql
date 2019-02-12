/* with tables it is often best to select only those columns that are relevant to the people reading the table. You can click on any column to make that the sort column.

A lot of users appreciate having the complete or a representative sample of the data used to build most of the charts in the dashboard. Including this data in a table at the bottom will allow them to explore further but clicking the Download Data from the chart menu on the upper-right of the chart while viewing it on the dashboard.*/
select
  user_id
  , platform
  , source
  , gender
  , signup_date
  , first_purchase_date
  , last_purchase_date
  , avg_purchase
  , num_purchases
  , num_gameplays
  , lifetime_days
from
  [user_summary]
where
  [user_mvp_level=MVP_Level]