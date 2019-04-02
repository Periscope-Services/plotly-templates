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

def percent(pct):
  return str(int(round(pct*100))) + '%'

df.columns = [c.lower() for c in df.columns]
y_col = [c for c in df.columns if c.startswith('y')][0]
ds_col = [c for c in df.columns if c.startswith('ds')][0]
agg = aggregation(ds_col)

pct_col = 'pct_change'
df[pct_col] = df[y_col].pct_change()

current = df.tail(1)
current_val = current[y_col]
current_pct = current[pct_col]

direction = ''
if current_pct > 0:
  direction = 'up ' + percent(abs(current_pct)) + ' from last ' + agg
elif current_pct < 0:
  direction = 'down ' + percent(abs(current_pct)) + ' from last ' + agg
else:
  direction = '

text = f'{column_name(y_col)} is {"up" if 
big_text = go.Scatter(
  x = [0],
  y = [.15],
  text = style_text(summary, font_size = '16px', font_weight = 'bold') + '<br><br>' + detail[0] + '<br>' + detail[1],
  textposition = 'middle center',
  mode = 'text',
  hoverinfo = 'none',
  xaxis = 'x2',
  yaxis = 'y2'
)

