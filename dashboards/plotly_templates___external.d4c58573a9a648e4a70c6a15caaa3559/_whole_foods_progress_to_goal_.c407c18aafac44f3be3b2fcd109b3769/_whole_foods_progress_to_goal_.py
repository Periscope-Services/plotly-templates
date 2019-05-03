import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import math

# racer = 'https://i.imgur.com/xk3PJy7.png'
racer = 'https://i.imgur.com/AKstrEW.png'

# GENERIC HELPER FUNCTIONS
def get_formatter(column):
  if '$' in column:
    return '$'
  elif '%' in column:
    return '%'
  else:
    return None

def format(num, formatter = None):
  if formatter is None:
    return abbrev(num)
  elif formatter == '$':
    return dollars(num)
  elif formatter == '%':
    return percent(num)
  
def tickformat(formatter):
  if formatter == '$':
    return '$.3s'
  elif formatter == '%':
    return '.0%'
  else:
    return '.3s'

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

def percent(pct):
  return str(int(round(pct*100))) + '%'

def pretty_percent(pct):
  fmt_pct = percent(pct)
#   if fmt_pct == '100%':
#     fmt_pct = '💯'
  if pct >= 1:
    fmt_pct = f'🎊<br><br>{fmt_pct}'
  return fmt_pct

def number_overlay(text):
  axis_setting = dict(range=[-1,1], showline=False, ticks='', showticklabels=False, showgrid=False, zeroline=False, fixedrange=True, autorange=False)
  annotation = dict(x=0, y=0, ax=0, ay=0, text=text)
  margin = dict(t=60,l=0,r=0)
  layout = go.Layout(xaxis=axis_setting,yaxis=axis_setting,annotations=[annotation],margin=margin)
  fig=go.Figure(data=[], layout=layout)
  periscope.plotly(fig, config={'displayModeBar':False})

def style_text(text, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<span style="{style}">{text}</span>'

def rgb_from_hex(hex):
  h = hex.lstrip('#')
  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

def rgba_from_hex(hex, alpha):
  rgb = rgb_from_hex(hex)
  return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'

def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

color = '#1c6cab'

df.columns = [c.upper() for c in df.columns]
x_column = [c for c in df.columns if c.startswith('X')][0]
current_col = [c for c in df.columns if c.startswith('CURRENT')][0]
goal_col = [c for c in df.columns if c.startswith('GOAL')][0]

road = go.Bar(
  x=df[goal_col],
  y=df[x_column],
  marker=dict(color='#B0B0AE'),
  orientation='h',
  name='Goal'
)

progress = go.Bar(
  x=df[current_col],
  y=df[x_column],
  marker=dict(color='#4569A5'),
  orientation='h',
  name='Current'
)

divider_line = go.Bar(
  x=df[goal_col],
  y=df[x_column],
  marker=dict(color='#DFB762'),
  orientation='h',
  width=.05,
  hoverinfo='none'
)

formatter = get_formatter(current_col)

images = []
for idx, row in df.iterrows():
    checker = {
        'source': 'https://i.imgur.com/0TY9CN4.png',
        'xref': 'x',
        'yref': 'y',
        'x': row[goal_col],
        'y': row[x_column],
        'xanchor': 'center',
        'yanchor': 'middle',
        'sizex': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 8.5, 
        'sizey': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 8.5
      }
    
    car = {
        'source': racer,
        'xref': 'x',
        'yref': 'y',
        'x': row[current_col],
        'y': row[x_column],
        'xanchor': 'center',
        'yanchor': 'middle',
        'sizex': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 8, 
        'sizey': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 8
      }
    
    images.append(checker)
    images.append(car)
    
print(images)

layout = go.Layout(
  images=images,
 	font = {
    'color': '#000000'
  },
  barmode='overlay',
  showlegend = False,
  margin=dict(
    l=50,
    r=0,
    t=0,
    b=40
  ),
  yaxis=dict(showline=False, showgrid=False, zeroline=False),
  xaxis=dict(showgrid=True, tickformat=tickformat(formatter), hoverformat=tickformat(formatter)),

)

fig = dict(data=[road, divider_line, progress], layout=layout)

periscope.plotly(fig)