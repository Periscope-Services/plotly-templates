import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import math

racer = 'http://images4.fanpop.com/image/photos/23000000/sonic-runs-not-that-type-of-run-sonic-the-hedgehog-23028548-2500-1875.png'
finish = 'https://i.imgur.com/2xo9Iqm.png'
ring = 'https://i.imgur.com/JO1dCCd.png'

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
  marker=dict(color='#91FC11'),
  orientation='h',
  name='Goal'
)

progress = go.Bar(
  x=df[current_col],
  y=df[x_column],
  marker=dict(color='#D86C18'),
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
        'source': finish,
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
        'sizex': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 6, 
        'sizey': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 6
      }
    images.append(checker)
    
    checkpoint_position = row[current_col] + .1 * max(df[current_col].max(), df[goal_col].max())
    while(True):
      checkpoint = {
        'source': ring,
        'xref': 'x',
        'yref': 'y',
        'x': checkpoint_position,
        'y': row[x_column],
        'xanchor': 'center',
        'yanchor': 'middle',
        'sizex': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 15, 
        'sizey': 1.0 * max(df[current_col].max(), df[goal_col].max()) / 15
      }
      images.append(checkpoint)
      checkpoint_position = checkpoint_position + .1 * max(df[current_col].max(), df[goal_col].max())
      print(checkpoint_position)
      if checkpoint_position > row[goal_col]:
        break

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

fig = dict(data=[road, progress], layout=layout)

periscope.plotly(fig)