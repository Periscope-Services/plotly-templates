# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go

line = go.Scatter(
  x = df['week'],
  y = df['count'],
  name = 'Signups',
  mode = 'lines',
  line = {
    'shape': 'spline',
    'smoothing': 1.3
  }
)

layout = go.Layout()

fig = dict(data = [line], layout = layout)

periscope.plotly(fig)
