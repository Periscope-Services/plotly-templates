import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

def format(column):
  if column.startswith('Y$'):
    return '$s'
  elif column.startswith('Y%'):
    return '.0%'
  else:
    return 's'
  
def unique_vals(df, column):
  return df.groupby(column).size().reset_index()[column]

# get the x, y, and series columns
def get_columns(df):
  x_column = [c for c in df.columns if c.startswith('X')][0]
  y_column = [c for c in df.columns if c.startswith('Y')][0]
  series_columns = [c for c in df.columns if c.startswith('S_')]
  unique_series = unique_vals(df, series_columns) if len(series_columns) > 0 else None
  return x_column, y_column, series_columns, unique_series

df.columns = [c.upper() for c in df.columns]
x_column, y_column, series_columns, unique_series = get_columns(df)
has_series = unique_series is not None
showlegend = has_series

data = []


# if no series -- create the traces for each y value and only display the first one
if not has_series:
  trace = go.Scatter(
	  x=df[x_column],
    y=df[y_column],
    name=column_name(y_column)
  )
  data.append(trace)
    
# if series -- create the traces for each series for each y value, still only displaying series for the first y value
else:
  for idx_series, series in unique_series.iterrows():
    query = ' & '.join(f'{col} == "{series[{col}].iloc[0]}"' for col in series_columns)
    df_series = df.query(query)
    trace = go.Scatter(
      x=df_series[x_column],
      y=df_series[y_column],
      name=f'{", ".join([series[{col}].iloc[0] for col in series_columns])}'
    )
    data.append(trace) 

layout = {
  'showlegend': showlegend,
  'yaxis': {
    'type': 'log',
    'title': column_name(y_column)
  },
  'xaxis': {
    'title': column_name(x_column)
  },
  'margin': {
    't': 20,
    'b': 50,
    'l': 60,
    'r': 10
  }
}

fig = dict(data=data, layout=layout)

# Use Periscope to visualize a dataframe by passing the data to periscope.output()
periscope.plotly(fig)