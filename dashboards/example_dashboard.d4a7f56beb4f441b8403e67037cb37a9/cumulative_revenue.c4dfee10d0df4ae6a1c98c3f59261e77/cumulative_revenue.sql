-- Use number overlays to display text on a dashboard - https://doc.periscopedata.com/article/graph-like-chart-types#content

select
  sum(price) as revenue
from
  periscope_views.purchases
where
-- Apply Custom filters. Create filters on the Dashboard first, then call them in the query with syntax [column=filter_name] as seen below. https://doc.periscopedata.com/article/custom-filters
  [platform=Device]