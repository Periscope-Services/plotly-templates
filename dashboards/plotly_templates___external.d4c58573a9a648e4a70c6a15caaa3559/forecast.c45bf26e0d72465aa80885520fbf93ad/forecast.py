# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go

def aggregation(df):
  return df['aggregation'].iloc[0]

df.columns = [c.lower() for c in df.columns]
df['y'] = pd.to_numeric(df['y'])

m = Prophet()
m.fit(df[['ds','y']])

agg = aggregation(df)
if agg = 'day':
  future = m.make_future_dataframe(periods=365)
elif agg = 'week':
  future = m.make_future_dataframe(periods=365)
elif agg = 'month':
  future = m.make_future_dataframe(periods=12, freq='M')

forecast = m.predict(future)


# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.table(df)
