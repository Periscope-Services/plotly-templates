import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go

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
  showlegend = False
)

fig = {
  'data': data,
  'layout': layout
}

periscope.plotly(fig)