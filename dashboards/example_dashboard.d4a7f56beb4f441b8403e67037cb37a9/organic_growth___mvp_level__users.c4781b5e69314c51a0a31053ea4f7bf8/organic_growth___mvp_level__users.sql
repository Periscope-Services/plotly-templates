select
  [us.signup_date:date:aggregation]
  , count(distinct us.user_id) as new_users
from -- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
  [user_summary as us]
  left join periscope_views.ad_spend a on
    us.signup_date = [a.created_at:date]
    -- <--- Use built in date formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
where
  source = 'organic'
  and
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
[user_mvp_level=MVP_Level]
group by
  1