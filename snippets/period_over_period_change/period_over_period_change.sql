-- this is a parameterized snippet. in the title name above, you can use comma (,) separated parameters in parentheses () to dynamically sub out different values in the SQL. This allow you to use this definition over and over easily with different data sets. If you make changes to the snippet, the changes are applied to any chart that is using it. hover over the snippet name for details

-- more info at https://doc.periscopedata.com/article/parameterized-sql-snippets#article-title

-- this snippet was sourced from the Periscope Community: https://community.periscopedata.com/t/36k5b5/chart-type-period-over-period-change  

select
  date
  , [field]
  , case
    when lag([field]) over(order by date) is null
      then null
    else 1.0 *[field] / lag([field]) over(order by date) - 1
  end as period_over_period_change_perc
  , case
    when lag([field]) over(order by date) is null
      then null
    else [field] - lag([field]) over(order by date) - 1
  end as period_over_period_change_value
  , case
    when lag([field]) over(order by date) is null
      then null
    else (case when lag([field]) over(order by date) > [field] then 'negative' else 'positive' end)
  end as period_over_period_change_direction
from
  (
    select
      [field]
      , [[date]:[aggregation]] as date
    from
      [table]
  )