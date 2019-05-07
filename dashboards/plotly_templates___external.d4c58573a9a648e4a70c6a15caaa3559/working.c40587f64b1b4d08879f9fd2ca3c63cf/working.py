# PERISCOPE PROGRESS TO GOAL TEMPLATE
# SQL output should have 2 columns:
#    1) current: the currently attained value
#    2) goal: the goal value
# 	 optionally apply dollar formatting by naming the columns current_$ and goal_$

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

# formats a number based on its formatter ($ or %)
def format(num, formatter = None):
  if formatter is None:
    return abbrev(num)
  elif formatter == '$':
    return dollars(num)
  elif formatter == '%':
    return percent(num)

# formats a number to dollars
def dollars(num):
  num = float('{:.3g}'.format(float(num)))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '${}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

# makes a number human readable e.g. 100000 -> 100K
def abbrev(num):
  num = float('{:.3g}'.format(float(num)))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

# formats a number to a percent
def percent(pct):
  return str(int(round(pct*100))) + '%'

# adds flair to a percent if it's above 100
def pretty_percent(pct):
  fmt_pct = percent(pct)
#   if fmt_pct == '100%':
#     fmt_pct = '💯'
  if pct >= 1:
    fmt_pct = f'🎊<br><br>{fmt_pct}'
  return fmt_pct

# prints text in the center of the plot
def number_overlay(text):
  axis_setting = dict(range=[-1,1], showline=False, ticks='', showticklabels=False, showgrid=False, zeroline=False, fixedrange=True, autorange=False)
  annotation = dict(x=0, y=0, ax=0, ay=0, text=text)
  margin = dict(t=60,l=0,r=0)
  layout = go.Layout(xaxis=axis_setting,yaxis=axis_setting,annotations=[annotation],margin=margin)
  fig=go.Figure(data=[], layout=layout)
  periscope.plotly(fig, config={'displayModeBar':False})

# returns css-styled text
def style_text(text, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<span style="{style}">{text}</span>'

# translates hex code to RGB values
def rgb_from_hex(hex):
  h = hex.lstrip('#')
  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

# translates RGB values to hex code
def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

# translates hex code to RGB values with alpha
def rgba_from_hex(hex, alpha):
  rgb = rgb_from_hex(hex)
  return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'

def style_link(text, link, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<a href="{link}" style="{style}">{text}</a>'

color = '#1c6cab'


df.columns = [c.upper() for c in df.columns]

is_valid = True
if len([c for c in df.columns if c.startswith('CURRENT')]) == 0:
  is_valid = False
if len([c for c in df.columns if c.startswith('GOAL')]) == 0:
  is_valid = False
  
if not is_valid:
  current = 1000
  goal = 2000
  formatter = '$'
  annotation = {
    'x': 0.5,
    'y': 0.55,
    'ax': 0,
    'ay': 0,
    'text': style_link('DUMMY<br><br><br><br>DATA<br><br><br><br>EXAMPLE', 'https://community.periscopedata.com/', font_size='60px', font_weight='bold', color='rgba(0, 0, 0, .25)'),
    'showarrow': False,
    'textangle': -25
  }

else:
  # get current and goal values
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
  color = '#00be11'


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

annotations = [
		{
      'x': 0.5,
      'y': 0.55,
      'ax': 0,
      'ay': 0,
      'text': style_text(pretty_percent(pct), font_size='32px', font_weight='bold') + '<br><br>' + style_text('Goal: ' + goal_formatted, font_size='18px')
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

if not is_valid:
  annotations.append(annotation)

layout = go.Layout(
 	font = {
    'color': '#000000'
  },
  showlegend = False,
  margin = {
    't': 30,
    'b': 30,
    'l': 30,
    'r': 30
  },
  annotations = annotations
)

fig = dict(data=[donut], layout=layout)

periscope.plotly(fig)
