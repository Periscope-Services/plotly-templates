/* x value prefixed with 'x'
   y value(s) prefixed with 'y' -- if $ or %, prefix with 'y$' or 'y%'
   series value(s) prefixed with 's'
*/
     
with
  purchases as (
    select
      [created_at:aggregation] as date
      , platform
      , count(1) as num_purchases
      , round(sum(price), 0) as sum_purchases
    from
      public.purchases
    group by
      1
      , 2
  )
  , gameplays as (
    select
      [created_at:aggregation] as date
      , platform
      , count(1) as num_gameplays
    from
      public.gameplays
    group by
      1
      , 2
  )
select
  coalesce(p.date, g.date) as x_date
  , coalesce(p.platform, g.platform) as s_platform
  , sum_purchases as "y$_revenue"
  , num_purchases as y_purchases
  , num_gameplays as y_plays
  , 1.0 * num_purchases / num_gameplays as "y%_conversion_rate"
  , 1.0 * sum_purchases / num_purchases as "y$_avg_purchase"
from
  purchases p
  full join gameplays g on
    p.date = g.date
    and p.platform = g.platform
order by
  1