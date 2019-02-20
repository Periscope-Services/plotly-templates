from collections import namedtuple
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import math

# GENERIC HELPER FUNCTIONS
def dollars(num):
  num = float('{:.3g}'.format(float(num)))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '${}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

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

data = row_as_tuple(df.iloc[[0]])
current = data.current
goal = data.goal
pct = 1.0 * current / goal

donut = go.Pie(
 	values = [current, goal - current if goal > current else 0],
  marker = {
    'colors': ['rgb(28,108,171)', 'rgba(28,108,171,0.2)']
  },
  hole = .8,
  textinfo='none',
  hoverinfo='none',
  sort=False
)

x = .5 * (1 + math.cos(math.radians((1 - pct) * 360 + 90)))
y = .5 * (1 + math.sin(math.radians((1 - pct) * 360 + 90)))
xsign = -1 if pct <= .5 else 1
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
      'text': style_text(percent(pct), font_size='32px', font_weight='bold') + '<br><br>' + style_text('Goal: ' + dollars(goal), font_size='18px')
    },
    {
      'x': x,
      'y': y,
      'ax': xsign * 20,
      'ay': ysign * 20,
    	'arrowcolor': 'rgba(0,0,0,0)',
      'text': style_text(dollars(current), font_size='14px', font_weight='bold')
    }
  ]
)

fig = dict(data=[donut], layout=layout)

periscope.plotly(fig)
