# SQL output should have two columns:
#   1) date
#   2) kpi -- this is the KPI value to display. if it's a dollar or percentage value, call it kpi_$ or kpi_% to apply formatting

from collections import namedtuple
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

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
  axis_setting = dict(range=[-1,1], showline=False, ticks='', showticklabels=False, showgrid=False, zeroline=False, fixedrange=True)
  annotation = dict(x=0, y=0, ax=0, ay=0, text=text)
  margin = dict(t=60)
  layout = go.Layout(xaxis=axis_setting,yaxis=axis_setting,annotations=[annotation],margin=margin)
  fig=go.Figure(data=[], layout=layout)
  periscope.plotly(fig, config={'displayModeBar':False})

def style_text(text, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<span style="{style}">{text}</span>'

def style_link(text, link, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<a href="{link}" style="{style}">{text}</a>'

def row_as_tuple(df):
  df.columns = [c.lower() for c in df.columns]
  dictionary = df.to_dict(orient='records')[0]
  return namedtuple('Tuple', dictionary.keys())(*dictionary.values())

def no_data():
  msg = 'No data to display.'
  number_overlay(style_text(msg, font_size="18px"))

# CHART-SPECIFIC STUFF

def rgb_from_hex(hex):
  h = hex.lstrip('#')
  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

def gradient(value, scale, colors):
  min = scale[0]
  max = scale[1]
  if value < min: 
    value = min
  elif value > max:
    value = max
  pct = 1.0 * (value - min) / (max - min)
  min_color = rgb_from_hex(colors[0])
  max_color = rgb_from_hex(colors[1])
  rgb = tuple(((int(round(pct * (max_color[i] - min_color[i]) + min_color[i])))) for i in range(0,3))
  return rgb_to_hex(rgb)

if df.size==0:
	no_data()

else:
  df.columns = [c.upper() for c in df.columns]
  kpi_col = [c for c in df.columns if c.startswith('KPI')][0]
  formatter = get_formatter(kpi_col)
  df.sort_values(by='DATE', ascending=False, inplace=True)
  current_val = df[kpi_col].iloc[0]
  prior_val = df[kpi_col].iloc[1]
  percentage_change = 1.0 * current_val / prior_val - 1 if prior_val > 0 else None
  indicator = '▲' if current_val > prior_val else '▼'
  kpi_change = indicator + ' ' + percent(percentage_change) + ' From Prior Period'
  color = gradient(percentage_change, [-.25, .25], ['#ff0000', '#00be11'])
  
  text = (
    style_text(format(current_val, formatter), font_size='50px', font_weight='bold') +
    '<br><br>' +
    style_text(kpi_change, font_size='16px', color=color)
  )
  
  number_overlay(text)