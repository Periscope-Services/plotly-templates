select t.* from (select
  [created_at:month] as date
  --Use built in currency formatter. https://doc.periscopedata.com/article/composing-sql-formatters
  , [sum(price):$] as revenue
from
  periscope_views.purchases
where
  -- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
  -- See this doc to learn how to add a filter to the dashboard: https://doc.periscopedata.com/article/add-remove-filters
  [platform=Device]
group by
  created_at) t 
--use built in date formatter: https://doc.periscopedata.com/article/composing-sql-formatters
where [date:ytd]