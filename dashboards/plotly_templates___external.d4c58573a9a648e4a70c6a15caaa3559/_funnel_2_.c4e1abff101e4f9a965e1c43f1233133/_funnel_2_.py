import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go

def label(idx, phase, value, max_value, max_idx):
  label = f'<b>{phase}</b> - {"{:,}".format(value)}'
  if idx != max_idx:
    label += f'<br>{"{:.0%}".format(1.0 * value/max_value)}'
  return label

df.columns = [c.lower() for c in df.columns]
phase_col = 'phase'
value_col = 'value'

maximum = df[value_col].max()

buffer = go.Bar(
  x = 1.0 * (maximum - df[value_col]) / 2,
  y = df[phase_col],
  marker = {
    'color': 'rgba(0,0,0,0)'
  },
  orientation = 'h'
)

funnel = go.Bar(
  x = df[value_col],
  y = df[phase_col],
  orientation = 'h'
)

data = [buffer, funnel, buffer]

layout = go.Layout(
  barmode = 'stack',
  showlegend = False,
  margin = {
    't': 0,
    'l': 0,
    'r': 0,
    'b': 0
  },
  xaxis = {
    'showline': False,
    'ticks': '',
    'showticklabels': False,
    'showgrid': False,
    'zeroline': False,
    'fixedrange': True
  },
  yaxis = {
    'showline': False,
    'ticks': '',
    'showticklabels': False,
    'showgrid': False,
    'zeroline': False,
    'fixedrange': True
  },
  annotations = [
    {
      'x': 1.0 * maximum / 2,
      'y': row[phase_col],
      'ax': 0,
      'ay': 0,
      'text': label(idx,row[phase_col],row[value_col],maximum, len(df) - 1)
    } for idx, row in df.iterrows()
  ]
)

fig = {
  'data': data,
  'layout': layout
}

periscope.plotly(fig)