# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

def format(column):
  if column.startswith('y$'):
    return '$s'
  elif column.startswith('y%'):
    return '.0%'
  else:
    return 's'
  
def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

def aggregation(df):
  return df['aggregation'].iloc[0]

df.columns = [c.lower() for c in df.columns]
y_col = [c for c in df.columns if c.startswith('y')][0]

df['y'] = pd.to_numeric(df[y_col])

m = Prophet()
m.fit(df[['ds','y']])

agg = aggregation(df)

if agg == 'hour':
  future = m.make_future_dataframe(periods=72, freq='H')
elif agg == 'day':
	future = m.make_future_dataframe(periods=30)
elif agg == 'week':
  future = m.make_future_dataframe(periods=365)
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
    'color': '#0472B2'
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
    'color': '#9aceed'
  },
  line = {
    'width': 1
  },
  showlegend = False,
  hoverinfo = 'none',
  mode = 'lines'
)

yhat_upper = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat_upper'],
  fill='tonexty',
  marker = {
    'color': '#9aceed'
  },
  line = {
    'width': 1
  },
  name = 'Margin of Error',
  hoverinfo = 'none',
  mode = 'lines'
)

actual = go.Scatter(
  x = df['ds'],
  y = df['y'],
  mode = 'markers',
  marker = {
    'color': '#000000',
    'size': 4
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
    't': 40,
    'b': 50,
    'l': 60,
    'r': 10
  }
)
data = [yhat_lower, yhat_upper, yhat, actual]
fig = dict(data = data, layout = layout)
periscope.plotly(fig)
