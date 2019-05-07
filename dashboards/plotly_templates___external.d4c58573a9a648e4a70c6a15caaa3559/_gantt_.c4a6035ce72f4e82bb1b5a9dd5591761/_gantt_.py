import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

# Create and assign list of column names
df.columns = [c.title() for c in df.columns]

# Use figure factory to create gantt chart
fig = ff.create_gantt(df)

periscope.plotly(fig)