# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

def aggregation(df):
  return df['aggregation'].iloc[0]

df.columns = [c.lower() for c in df.columns]
df['y'] = pd.to_numeric(df['y'])

m = Prophet()
m.fit(df[['ds','y']])

future = m.make_future_dataframe(periods=365)
agg = aggregation(df)
if agg == 'day':
  future = future
elif agg == 'week':
  future = future[future['ds'].dt.weekday == 0]
elif agg == 'month':
  future = future[future['ds'].dt.day == 1]
elif agg == 'quarter':
  future = future[(future['ds'].dt.month % 3 == 1) & (future['ds'].dt.day == 1)]
elif agg == 'year':
  future = future[(future['ds'].dt.month == 1) & (future['ds'].dt.day == 1)]

forecast = m.predict(future)


# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.table(df)
