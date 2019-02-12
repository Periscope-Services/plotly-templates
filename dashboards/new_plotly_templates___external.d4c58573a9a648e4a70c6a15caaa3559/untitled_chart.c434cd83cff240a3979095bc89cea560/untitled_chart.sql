select
  date
  , cookie as entity
  , rank
from
  [stackrank_dummy_data]
where
  [date=10days]
order by
  1