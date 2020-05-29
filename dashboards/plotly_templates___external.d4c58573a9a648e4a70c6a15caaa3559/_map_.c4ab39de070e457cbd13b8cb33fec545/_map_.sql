select
  id
  , [created_at:date] as s_date
  , latitude
  , longitude
from
  users
limit 50000