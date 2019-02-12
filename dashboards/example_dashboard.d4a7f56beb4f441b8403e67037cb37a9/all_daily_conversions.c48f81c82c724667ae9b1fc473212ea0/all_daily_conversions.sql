with
  signups as (
    select
    --Use built in date formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
      [us.signup_date:date:aggregation] as signup_date
      , count(distinct us.user_id) as signups
      , sum(
        case
          when us.num_purchases > 0
            then 1
          else 0
        end
      )
      as conversions
    from
    -- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
      [user_summary as us]
    group by
      signup_date
  )
select
  signup_date
  , conversions / cast(signups as float) as conversion_rate
from
  signups