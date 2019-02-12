--invoke R for advanced analysis and access to additional plotting options through plotting libraries. 

select
  user_id
  , platform
  , lifetime_days
from -- call views in periscope by enclosing them in brackets. Docs: https://doc.periscopedata.com/article/views#content
  [user_summary]
where
  lifetime_days > 1