/***********************************
SQL output should have two columns:
  1) date
  2) kpi -- this is the KPI value to display. if it's a dollar or percentage value, call it kpi_$ or kpi_% to apply formatting
***********************************/
select
  [created_at:month] as date
  , sum(price) as "kpi_$"
from
  periscope_views.purchases
group by
  1