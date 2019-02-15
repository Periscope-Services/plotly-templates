import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
from datetime import timedelta

def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

def format(column):
  if column.startswith('Y$'):
    return '$s'
  elif column.startswith('Y%'):
    return '.0%'
  else:
    return 's'

def get_columns(df):
  y_column = [c for c in df.columns if c.startswith('Y')][0]
  series_columns = [c for c in df.columns if c.startswith('S')]
  unique_series = unique_vals(df, series_columns) if len(series_columns) > 0 else None
  return y_column, series_columns, unique_series

def unique_vals(df, column):
  return df.groupby(column).size().reset_index()[column]

df.columns = [c.upper() for c in df.columns]
y_column, series_columns, unique_series = get_columns(df)
has_series = unique_series is not None
# showlegend = has_series

traces = []
for idx, series in unique_series.iterrows():
  query = ' & '.join(f'{col} == "{series[{col}].iloc[0]}"' for col in series_columns)
  df_series = df.query(query)
  traces.append(
    go.Box(
      y=df_series[y_column],
      boxpoints = False,
      name=f'{", ".join([series[{col}].iloc[0] for col in series_columns])}'
    )
  )

data = traces

layout = {
  'margin': {
    'l': 50,
    'r': 0,
    'b': 30,
    't': 0
  },
  'yaxis': {
    'title': column_name(y_column),
    'tickformat': format(y_column),
    'hoverformat': format(y_column)
  }
}

fig = dict(data=data, layout=layout)
periscope.plotly(fig)