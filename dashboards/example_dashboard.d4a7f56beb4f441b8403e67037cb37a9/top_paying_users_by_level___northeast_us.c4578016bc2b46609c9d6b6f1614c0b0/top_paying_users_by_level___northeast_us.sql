select
  user_mvp_level
  , case user_mvp_level
      when '500+_Platinum' then 1
      when '250+_Gold' then 2
      when '100+_Silver' then 3
    end as user_mvp_level_numeric
  , total_purchases
  , latitude
  , longitude
from 
-- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
  [user_summary]
where
  total_purchases >= 100
  and 
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
[platform=Device]