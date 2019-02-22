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

def rect(x0,y0,x1,y1,fillcolor = None, bordercolor = None):
  return {
    'type': 'rect',
    'xref': 'x',
    'yref': 'y',
    'fillcolor': fillcolor if fillcolor else '#ffffff',
              'x0': x0,
              'y0': y0,
              'x1': x1,
              'y1': y1,
              'line': {
                  'color': bordercolor if bordercolor else 'rgba(0,0,0,0)',
              }
  }

def circle(x0,y0,x1,y1,fillcolor=None,bordercolor=None,borderwidth=1):
  return {
    'type': 'circle',
    'xref': 'x',
    'yref': 'y',
    'fillcolor': fillcolor if fillcolor else '#ffffff',
              'x0': x0,
              'y0': y0,
              'x1': x1,
              'y1': y1,
              'line': {
                  'color': bordercolor if bordercolor else 'rgba(0,0,0,0)',
                	'width': borderwidth
              }
  }

shapes = []
# shapes.append({
#   'type': 'circle',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'blue',
#             'x0': 0,
#             'y0': 0,
#             'x1': 1,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 1)',
#               	'width': 5
#             }
# })
# shapes.append({
#   'type': 'circle',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'blue',
#             'x0': 1.5,
#             'y0': 0,
#             'x1': 2.5,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 1)',
#               'width': 5
#             }
# })
# shapes.append({
#   'type': 'rect',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'blue',
#             'x0': .5,
#             'y0': 0,
#             'x1': 2,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 1)',
#               'width': 5
#             }
# })
# shapes.append({
#   'type': 'circle',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'white',
#             'x0': 0,
#             'y0': 0,
#             'x1': 1,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 0)',
#             }
# })
# shapes.append({
#   'type': 'circle',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'white',
#             'x0': 1.5,
#             'y0': 0,
#             'x1': 2.5,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 0)',
#             }
# })
# shapes.append({
#   'type': 'rect',
#   'xref': 'x',
#   'yref': 'y',
#   'fillcolor': 'white',
#             'x0': .5,
#             'y0': 0,
#             'x1': 2,
#             'y1': 1,
#             'line': {
#                 'color': 'rgba(50, 171, 96, 0)',
#             }
# })

shapes.append(rect(0,0,3,1,fillcolor=None,bordercolor='blue'))
shapes.append(circle(-.2,-.2,1.2,1.2,fillcolor='rgba(0,0,0,0)',bordercolor='blue',borderwidth=28))

layout = go.Layout(
  xaxis={'range': [-1,4], 'autorange':False},
  yaxis={'range': [-1,4], 'autorange':False},
  shapes=shapes
)

fig = dict(data=[go.Scatter(x=[.5],y=[.5])], layout=layout)

periscope.plotly(fig)
