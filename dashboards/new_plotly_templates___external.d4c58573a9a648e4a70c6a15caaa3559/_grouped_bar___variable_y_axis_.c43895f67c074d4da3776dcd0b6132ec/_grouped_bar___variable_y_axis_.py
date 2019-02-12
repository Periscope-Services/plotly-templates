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

# get the x, y, and series columns
def get_columns(df):
  x_column = [c for c in df.columns if c.startswith('X')][0]
  y_columns = [c for c in df.columns if c.startswith('Y')]
  series_columns = [c for c in df.columns if c.startswith('S')]
  if len(series_columns) > 0:
  	unique_series = df.groupby(series_columns).size().reset_index()[series_columns]
  else:
    unique_series = None
  return x_column, y_columns, series_columns, unique_series

def button(y_col, y_columns, unique_series = None):
  return {
    'label': column_name(y_col),
    'method': 'update',
    'args': [
      {
        'visible': [c==y_col for c in y_columns for i in range(0, 1 if unique_series is None else len(unique_series))]
      },
      {
        'yaxis': {
          'tickformat': format(y_col),
          'hoverformat': format(y_col)
        }
      }
    ]
  }
      

# force consistent casing for columns
df.columns = [c.upper() for c in df.columns]
x_column, y_columns, series_columns, unique_series = get_columns(df)
has_series = unique_series is not None
showlegend = has_series

data = []
buttons = []

for idx, y_col in enumerate(y_columns):
  buttons.append(button(y_col, y_columns, unique_series=unique_series))
  
  # if no series -- create the traces for each y value and only display the first one
  if not has_series:
    trace = go.Bar(
			x=df[x_column],
      y=df[y_col],
      name=column_name(y_col),
      visible=(idx==0)
    )
    data.append(trace)
    
  # if series -- create the traces for each series for each y value, still only displaying series for the first y value
  else:
    for idx_series, series in unique_series.iterrows():
      query = ' & '.join(f'{col} == "{series[{col}].iloc[0]}"' for col in series_columns)
      df_series = df.query(query)
      trace = go.Bar(
        x=df_series[x_column],
        y=df_series[y_col],
        name=f'{", ".join([series[{col}].iloc[0] for col in series_columns])}',
        visible=(idx == 0)
      )
      data.append(trace) 

updatemenus = list([
  {
    'active': 0,
    'buttons': buttons,
    'x': -.1,
    'y': 1.25,
    'xanchor': 'left',
    'yanchor': 'top',
    'bgcolor': '#FFFFFF'
  }
])

first_y = y_columns[0]
xaxis = {'title': column_name(x_column)}

# if x value is a date, then add the quick-filter options for dates
if isinstance(df[x_column].iloc[0], datetime.date):
  duration = (df[x_column].max() - df[x_column].min()).days
  month_buttons = [dict(count=x, label=str(x)+'m', step='month', stepmode='backward') for x in [1,3,6] if x * 30 <= duration]
  
  xaxis['rangeselector'] = {
    'buttons': list(month_buttons + [{'step': 'all'}]) if len(month_buttons) > 0 else None, 
    'xanchor': 'right',
    'yanchor': 'top',
    'x': 1,
    'y': 1.2
  }
             
layout = {
  'showlegend': showlegend,
  'updatemenus': updatemenus,
  'yaxis': {
    'tickformat': format(first_y),
    'hoverformat': format(first_y)
  },
  'xaxis': xaxis,
  'margin': {
    't': 20,
    'b': 50,
    'l': 10,
    'r': 10
  }
}

fig = dict(data=data, layout=layout)

# Use Periscope to visualize a dataframe by passing the data to periscope.output()
periscope.plotly(fig)
