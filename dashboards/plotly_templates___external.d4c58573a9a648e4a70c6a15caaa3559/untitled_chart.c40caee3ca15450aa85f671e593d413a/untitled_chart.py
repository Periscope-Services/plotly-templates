from collections import namedtuple
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

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

layout = go.Layout(
  showlegend = False,
  margin = {
    't': 10,
    'b': 10,
    'l': 10,
    'r': 10
  },
  annotations = [
		{
      'x': 0.5,
      'y': 0.5,
      'ax': 0,
      'ay': 0,
      'text': style_text(percent(pct), font_size='48px', font_weight='bold') + '<br><br><br>' + style_text('Goal: ' + dollars(goal), font_size='26px')
    },
    {
      'x': 1 + .5 * np.cos(np.pi - 2 * np.pi * (float(current) % goal /goal)),
      'y': 1 + .5 * np.sin(np.pi - 2 * np.pi * (float(current) % goal / goal)),
      'ax': 0,
      'ay': 0,
      'text': dollars(current)
    }
  ]
)

fig = dict(data=[donut], layout=layout)

periscope.plotly(fig)
