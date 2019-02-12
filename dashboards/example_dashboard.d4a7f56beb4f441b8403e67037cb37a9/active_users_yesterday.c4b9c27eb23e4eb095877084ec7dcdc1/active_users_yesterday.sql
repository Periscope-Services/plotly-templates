-- Use number overlays to display text on a dashboard - https://doc.periscopedata.com/article/graph-like-chart-types#content

select
  count(distinct users.id)
from
  periscope_views.gameplays
  join periscope_views.users on
    gameplays.user_id = users.id
where
--Use built in date formatter- [date_column:date]  https://doc.periscopedata.com/article/composing-sql-formatters
  [gameplays.created_at:yesterday]
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
  and [gameplays.platform=device]