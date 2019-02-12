-- ▲ Click the title to see how filter names name can be dynamically substituted.

select
  platform
  , [avg(total_purchases/case lifetime_days when 0 then 1 else lifetime_days end):$] as daily_arppu
-- ^ Use built in currency formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
  , [avg(total_purchases):$] as lifetime_arppu
-- ^ Use built in currency formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
from
-- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
  [user_summary]
where
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
[user_mvp_level=MVP_Level]
group by
  platform
order by
  platform