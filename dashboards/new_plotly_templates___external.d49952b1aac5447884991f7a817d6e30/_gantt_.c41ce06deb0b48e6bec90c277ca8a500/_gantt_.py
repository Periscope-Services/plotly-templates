import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

community_post = ''
dummy_df = pd.DataFrame()

def style_link(text, link, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<a href="{link}" style="{style}">{text}</a>'

def plot(df, annotation=None):
  # Create and assign list of column names
  df.columns = [c.title() for c in df.columns]

  # Use figure factory to create gantt chart
  fig = ff.create_gantt(df)
  layout = go.Layout()
  if annotation is not None:
    fig['annotations'] = [annotation]
  periscope.plotly(fig)
  
