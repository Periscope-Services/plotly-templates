import pandas as pd 
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

df.columns = [c.lower() for c in df.columns]
y_col = [c for c in df.columns if c.startswith('y')][0]
ds_col = [c for c in df.columns if c.startswith('ds')][0]
agg = aggregation(ds_col)

df['pct_change'] = df[y_col].pct_change()

