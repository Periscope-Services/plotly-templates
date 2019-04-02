import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

color = '#02b9e5'

def get_formatter(column):
  if '$' in column:
    return '$'
  elif '%' in column:
    return '%'
  else:
    return None

def tickformat(column):
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

def format(num, formatter = None):
  if formatter is None:
    return abbrev(num)
  elif formatter == '$':
    return dollars(num)
  elif formatter == '%':
    return percent(num)

def dollars(num):
  num = float('{:.3g}'.format(float(num)))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '${}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def abbrev(num):
  num = float('{:.3g}'.format(float(num)))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def style_text(text, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<span style="{style}">{text}</span>'

df.columns = [c.lower() for c in df.columns]
y_col = [c for c in df.columns if c.startswith('y')][0]
ds_col = [c for c in df.columns if c.startswith('ds')][0]
agg = aggregation(ds_col)

pct_col = 'pct_change'
df[pct_col] = df[y_col].pct_change()

current = df.tail(1)
current_val = current[y_col].iloc[0]
current_pct = current[pct_col].iloc[0]

direction = ''
if current_pct > 0:
  direction = ',<br><br>up ' + style_text(percent(abs(current_pct)), color='#00be11', font_weight='bold') + ' since last ' + agg
elif current_pct < 0:
  direction = ',<br><br>down ' + style_text(percent(abs(current_pct)), color='#ff0000', font_weight='bold') + ' since last ' + agg
  
direction = style_text(direction, font_size = '16px')
  
fmt = get_formatter(y_col)
summary = f'{column_name(y_col)}: {style_text(format(current_val, formatter=fmt), color=color, font_weight="bold")}{direction}.'

big_text = go.Scatter(
  x = [0],
  y = [.15],
  text = style_text(summary, font_size = '20px'),
  textposition = 'middle center',
  mode = 'text',
  hoverinfo = 'none',
  xaxis = 'x2',
  yaxis = 'y2'
)

bar = go.Bar(
  x = df[ds_col],
  y = df[y_col],
  name = column_name(y_col),
  xaxis = 'x1',
  yaxis = 'y1',
  marker = {
    'color': color
  }
)

data = [big_text, bar]

layout = go.Layout(
  font = {
    'color': '#000000'
  },
  showlegend = False,
  margin = {
    'l': 10,
    'r': 10,
    't': 20,
    'b': 20
  },
  xaxis2 = {
    'range': [-1, 1],
    'fixedrange': True,
    'autorange': False,
    'showline': False,
    'showticklabels': False,
    'showgrid': False,
    'zeroline': False,
    'ticks': ''
  },
  yaxis2 = {
    'domain': [0.6, 1],
    'range': [-1, 1],
    'fixedrange': True,
    'autorange': False,
    'showline': False,
    'showticklabels': False,
    'showgrid': False,
    'zeroline': False
  },
  xaxis = {
    'ticks': '',
    'showline': False,
    'showgrid': False,
    'zeroline': False,
    'fixedrange': True,
#     'showticklabels': False
  },
  yaxis = {
    'domain': [0, 0.6],
    'autorange': True,
    'hoverformat': tickformat(y_col),
    'fixedrange': True,
    'showline': False,
    'showticklabels': False,
    'showgrid': False,
    'zeroline': False
  }
)

fig = go.Figure(data=data, layout=layout)
periscope.plotly(fig)