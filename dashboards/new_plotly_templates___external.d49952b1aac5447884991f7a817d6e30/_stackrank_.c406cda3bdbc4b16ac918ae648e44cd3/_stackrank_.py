# PERISCOPE STACKRANK TEMPLATE
# SQL output should have 3 columns:
#    1) date: the date of the ranking
#    2) entity: the name of the thing being ranked
#		 3) rank: the entity's rank at that point in time
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from random import shuffle
from datetime import datetime, timedelta

# Generating dummy data in case SQL output is in the incorrect format
community_post = 'https://community.periscopedata.com/t/18s9z8'
current_date = datetime.now()

cookies = ['Thin Mints', 'Samoas' ,'Trefoils', 'Do-si-dos', 'Tagalongs']
vals = []

for i in range(0,10):
  date = current_date - timedelta(days=i)
  shuffle(cookies)
  for k in range(0, len(cookies)):
    vals.append({
      'date': date,
      'entity': cookies[k],
      'rank': k + 1
    })
dummy_df = pd.DataFrame(vals)

# HELPER FUNCTION
def style_link(text, link, **settings):
  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
  return f'<a href="{link}" style="{style}">{text}</a>'

# MAIN FUNCTION
def plot(df, annotation_msg=None):
  df.columns = [c.lower() for c in df.columns]

  # get distinct entities and dates
  entities = df.groupby(['entity']).size().reset_index()['entity']
  dates = df.groupby(['date']).size().reset_index()['date']


  traces = []
  annotations = []
  for entity in entities:
    entity_data = df.query('entity == @entity')

    # plot rank of entity on each date
    for date in dates:
      if date > entity_data['date'].min() and entity_data.query('date == @date').size == 0:
        new_row = pd.DataFrame({
          'date': [date],
          'entity': [entity],
          'rank': [None]
        })
        entity_data = entity_data.append(pd.DataFrame(new_row))
    entity_data.sort_values(by='date',inplace=True)
    trace = go.Scatter(
      x=entity_data['date'],
      y=entity_data['rank'],
      name=entity,
      text=entity_data['rank'].astype(str) + ' ' + entity,
      line={
        'width': 0.75
      },
      mode='markers+lines',
      hoverinfo='text',
      connectgaps=False,
      opacity=0.75,
      marker={
        'size': 7
      }
    )
    traces.append(trace)

    # plot a gray line to indicate drop offs from the ranking
    trace2 = go.Scatter(
      x=entity_data['date'],
      y=entity_data['rank'],
      mode='lines',
      line={
        'dash': 'dash',
        'color': '#afafaf',
        'width': 0.5
      },
      hoverinfo='none',
      connectgaps=True,
      opacity=0.5
    )
    traces.append(trace2)
    annotation = {
      'x': entity_data['date'].iloc[0],
      'y': entity_data['rank'].iloc[0] - 0.2,
      'ax': 0,
      'ay': 0,
      'text': f'<b style="font-size:12px">{entity}</b>'
    }
    annotations.append(annotation)
    
  if annotation_msg is not None:
    annotations.append(annotation_msg)

  layout = {
    'showlegend': False,
    'margin':{
      'l': 30,
      'r': 0,
      't': 20,
      'b': 30
    },
    'yaxis':{
      'showline': False,
      'ticks': '', 
      'showticklabels': False,
      'showgrid': False,
      'zeroline': False,
      'range': [df['rank'].max(), df['rank'].min()],
      'fixedrange': True,
      'tickmode': 'linear',
      'title': '<b>Ranking</b>'
    },
    'xaxis':{
      'ticks': '',
      'fixedrange': True,
      'title': '<b>Date</b>'
    },
    'annotations': annotations
  }

  fig = {
    'data': traces,
    'layout': layout

  }

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
  plot(dummy_df, annotation_msg=annotation)