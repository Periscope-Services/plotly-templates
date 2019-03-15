import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

df.columns = [c.title() for c in df.columns]
fig = ff.create_gantt(df, height=300, width=400)
fig['layout']['margin'] = {
  't': 80,
  'b': 20,
  'l': 60,
  'r': 20
}
periscope.plotly(fig)