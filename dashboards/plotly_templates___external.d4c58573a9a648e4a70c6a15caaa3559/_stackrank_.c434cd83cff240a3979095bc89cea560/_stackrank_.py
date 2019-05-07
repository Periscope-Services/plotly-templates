# PERISCOPE STACKRANK TEMPLATE
# SQL output should have 3 columns:
#    1) date: the date of the ranking
#    2) entity: the name of the thing being ranked
#		 3) rank: the entity's rank at that point in time
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

df.columns = [c.lower() for c in df.columns]

entities = df.groupby(['entity']).size().reset_index()['entity']
dates = df.groupby(['date']).size().reset_index()['date']
traces = []
annotations = []
for entity in entities:
  entity_data = df.query('entity == @entity')
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
