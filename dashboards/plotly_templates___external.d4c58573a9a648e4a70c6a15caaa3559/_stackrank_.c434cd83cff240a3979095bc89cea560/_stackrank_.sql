with
  dates as (
    select
      distinct date
    from
      [stackrank_dummy_data]
    order by
      1 desc
    limit 7
  )
select
  date
  , cookie as entity
  , rank
from
  [stackrank_dummy_data]
where
  date in (
    select
      date
    from
      dates
  )
order by
  1