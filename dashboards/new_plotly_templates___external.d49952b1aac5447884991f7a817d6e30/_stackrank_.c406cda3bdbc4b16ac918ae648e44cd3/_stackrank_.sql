select
  date
  , cookie as entity
  , rank
from
  [stackrank_dummy_data]
where
  [date=7days]
order by
  1