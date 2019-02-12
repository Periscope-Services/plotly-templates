import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

df.columns = [c.title() for c in df.columns]
fig = ff.create_gantt(df, height=300, width=400)
periscope.plotly(fig)