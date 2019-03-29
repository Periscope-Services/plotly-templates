# PERISCOPE FORECAST TEMPLATE
# SQL output should have 2 columns:
#    1) ds_aggregation: the date or datetime. name should be ds_hour, ds_day, ds_week, ds_month, ds_quarter, or ds_year. if you are using Periscope's aggregation filter, you can name it ds_[aggregation]

#    2) y_value: the value to forecast. name it whatever makes sense, e.g. y_signups, y$_revenue, etc. add the dollar sign ($) to format in dollars.


import pandas as pd 
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

def format(column):
  if column.startswith('y$'):
    return '$.3s'
  elif column.startswith('y%'):
    return '.0%'
  else:
    return '.3s'
  
def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

def aggregation(ds_col):
  return ds_col.split('_', 1)[1].lower()

def in_progress(dt, agg):
  now = datetime.datetime.now()
  if agg == 'hour':
    return (now.year == dt.year and now.month == dt.month and now.day == dt.day and now.hour == dt.hour)
  elif agg == 'day':
    return (now.year == dt.year and now.month == dt.month and now.day == dt.day)
  elif agg == 'week':
    return (now.year == dt.year and now.isocalendar()[1] == dt.isocalendar()[1])
  elif agg == 'month':
    return (now.year == dt.year and now.month == dt.month)
  elif agg == 'quarter':
    return (now.year == dt.year and int(now.month / 4) == int(dt.month / 4))
  elif agg == 'year':
    return (now.year == dt.year)

df.columns = [c.lower() for c in df.columns]
y_col = [c for c in df.columns if c.startswith('y')][0]
ds_col = [c for c in df.columns if c.startswith('ds')][0]
agg = aggregation(ds_col)

df['y'] = pd.to_numeric(df[y_col])
df['ds'] = df[ds_col]
df['in_progress'] = df.apply(lambda x: in_progress(x['ds'], agg), axis=1)

m = Prophet()
m.fit(df.query('in_progress == False')[['ds','y']])

if agg == 'hour':
  future = m.make_future_dataframe(periods=72, freq='H')
elif agg == 'day':
	future = m.make_future_dataframe(periods=30)
elif agg == 'week':
  future = m.make_future_dataframe(periods=183)
  future = future[future['ds'].dt.weekday == 0]
elif agg == 'month':
  future = m.make_future_dataframe(periods=365)
  future = future[future['ds'].dt.day == 1]
elif agg == 'quarter':
  future = m.make_future_dataframe(periods=365)
  future = future[(future['ds'].dt.month % 3 == 1) & (future['ds'].dt.day == 1)]
elif agg == 'year':
  future = m.make_future_dataframe(periods=731)
  future = future[(future['ds'].dt.month == 1) & (future['ds'].dt.day == 1)]

forecast = m.predict(future)

yhat = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat'],
  mode = 'lines',
  marker = {
    'color': '#3bbed7'
  },
  line = {
    'width': 3
  },
  name = 'Forecast',
)

yhat_lower = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat_lower'],
  marker = {
    'color': 'rgba(0,0,0,0)'
  },
  showlegend = False,
  hoverinfo = 'none',
)

yhat_upper = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat_upper'],
  fill='tonexty',
  fillcolor = 'rgba(231, 234, 241,.75)',
  name = 'Margin of Error',
  hoverinfo = 'none',
  mode = 'none'
)

actual = go.Scatter(
  x = df['ds'],
  y = df['y'],
  mode = 'markers',
  marker = {
    'color': '#fffaef',
    'size': 4,
    'line': {
      'color': '#000000',
      'width': .75
    }
  },
  name = 'Actual'
)

layout = go.Layout(
  yaxis = {
    'title': column_name(y_col),
    'tickformat': format(y_col),
    'hoverformat': format(y_col)
  },
  hovermode = 'x',
  xaxis = {
    'title': agg.title()
  },
  margin = {
    't': 20,
    'b': 50,
    'l': 60,
    'r': 10
  }
)
data = [yhat_lower, yhat_upper, yhat, actual]
fig = dict(data = data, layout = layout)
periscope.plotly(fig)
