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
  if annotation is not None:
    fig['layout']['annotations'] = [annotation]
  periscope.plotly(fig)
  
try:
  plot(df)
except Exception as e:
	print(e)
	annotation = {
    'x': 0.5,
    'y': 0.5,
    'ax': 0,
    'ay': 0,
    'xref': 'paper',
    'yref': 'paper',
    'text': style_link('DUMMY<br><br><br><br>DATA<br><br><br><br>EXAMPLE', community_post, font_size='60px', font_weight='bold', color='rgba(0, 0, 0, .25)'),
    'showarrow': False,
    'textangle': -25
  }
	plot(dummy_df, annotation=annotation)
