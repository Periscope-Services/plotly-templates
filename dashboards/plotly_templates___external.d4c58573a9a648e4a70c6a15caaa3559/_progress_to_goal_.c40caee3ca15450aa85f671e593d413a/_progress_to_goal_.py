from collections import namedtuple
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import math

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

def row_as_tuple(df):
  df.columns = [c.lower() for c in df.columns]
  dictionary = df.to_dict(orient='records')[0]
  return namedtuple('Tuple', dictionary.keys())(*dictionary.values())

def rgb_from_hex(hex):
  h = hex.lstrip('#')
  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

def rgba_from_hex(hex, alpha):
  rgb = rgb_from_hex(hex)
  return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'

color = '#1c6cab'

df.columns = [c.upper() for c in df.columns]
current_col = [c for c in df.columns if c.startswith('CURRENT')][0]
goal_col = [c for c in df.columns if c.startswith('GOAL')][0]
data = df.iloc[[0]]
current = data[current_col].iloc[0]
goal = data[goal_col].iloc[0]

formatter = get_formatter(current_col)
current_formatted = format(current, formatter)
goal_formatted = format(goal, formatter)

pct = 1.0 * current / goal
if pct > 1:
  color = '#37bf8d'


donut = go.Pie(
 	values = [current, goal - current if goal > current else 0],
  marker = {
    'colors': [color, rgba_from_hex(color, .2)]
  },
  hole = .8,
  textinfo='none',
  hoverinfo='none',
  sort=False
)

x = .5 * (1 + math.cos(math.radians(max((1 - pct), 0) * 360 + 90)))
y = .5 * (1 + math.sin(math.radians(max((1 - pct), 0) * 360 + 90)))
xsign = 1 if pct <= .5 else -1
ysign = 1 if pct <= .5 else -1

layout = go.Layout(
  showlegend = False,
  margin = {
    't': 30,
    'b': 30,
    'l': 30,
    'r': 30
  },
  annotations = [
		{
      'x': 0.5,
      'y': 0.55,
      'ax': 0,
      'ay': 0,
      'text': style_text(percent(pct) if percent(pct) != '100%' else '🎊  💯  🎉', font_size='32px', font_weight='bold') + '<br><br>' + style_text('Goal: ' + goal_formatted, font_size='18px')
    },
    {
      'x': x,
      'y': y,
      'ax': xsign * 10,
      'ay': ysign * 10,
    	'arrowcolor': 'rgba(0,0,0,0)',
      'text': style_text(current_formatted, font_size='14px', font_weight='bold')
    }
  ]
)

fig = dict(data=[donut], layout=layout)

periscope.plotly(fig)
