-- Use number overlays to display text on a dashboard
select
  sum(spend) as spend
from
  periscope_views.ad_spend
where
  --Use built in date formatter.  https://doc.periscopedata.com/article/composing-sql-formatters
  [created_at:month] = [getdate():month] - interval '1 month'