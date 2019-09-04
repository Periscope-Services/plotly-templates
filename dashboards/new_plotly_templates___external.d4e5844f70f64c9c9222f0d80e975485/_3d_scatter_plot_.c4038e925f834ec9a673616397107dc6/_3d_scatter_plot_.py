import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

trace = go.Scatter3d(
  x=df['x'],
  y=df['y'],
  z=df['z'],
  mode='markers',
  marker={
    'opacity': 0.8
  }
)
data=[trace]
layout = go.Layout(
  margin={
    'l': 0,
    'r': 0,
    't': 0,
    'b': 0
  }
)
fig = go.Figure(data=data, layout=layout)
periscope.plotly(fig, config={'scrollZoom': True})