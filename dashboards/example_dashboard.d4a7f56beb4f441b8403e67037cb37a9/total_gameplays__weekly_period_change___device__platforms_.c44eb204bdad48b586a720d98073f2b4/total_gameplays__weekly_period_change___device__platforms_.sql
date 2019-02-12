-- nest the original query as a sub query. Name the resulting table "plays"
with
  plays as (
    select
      created_at as new_date
      , count(*)
    from
      periscope_views.gameplays
    where
    -- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
      [platform=Device]
    group by
      1
  )
--  call the "period over period change" snippet. Observe the original values in parentheses: [period_over_period_change(table,field,date,aggregation)] vs the snippet reference below.

-- learn more @ https://community.periscopedata.com/t/36k5b5/chart-type-period-over-period-change

[period_over_period_change(plays,count,new_date,month)]