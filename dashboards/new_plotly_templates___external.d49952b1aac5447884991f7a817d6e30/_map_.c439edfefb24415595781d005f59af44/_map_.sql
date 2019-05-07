select
  id
  , [created_at:date] as s_date
  , latitude
  , longitude
from
  periscope_views.users
limit 50000