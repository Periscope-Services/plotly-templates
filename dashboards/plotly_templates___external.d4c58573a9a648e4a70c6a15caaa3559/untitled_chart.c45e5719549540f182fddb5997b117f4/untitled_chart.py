# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go
import math

def rgb_from_hex(hex):
  h = hex.lstrip('#')
  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

def gradient(value, scale, colors):
  min = scale[0]
  max = scale[1]
  if value < min: 
    value = min
  elif value > max:
    value = max
  pct = 1.0 * (value - min) / (max - min)
  min_color = rgb_from_hex(colors[0])
  max_color = rgb_from_hex(colors[1])
  rgb = tuple(((int(round(pct * (max_color[i] - min_color[i]) + min_color[i])))) 	for i in range(0,3))
  return rgb_to_hex(rgb)

def arc(offset, start, end):
  pct =  1.0 * (end - start) / 100
  color = gradient(pct, [0, 1], ['#ff0000', '#00be11'])
  return pct * offset

def color(end):
  pct =  1.0 * end / 100
  color = gradient(pct, [0, 1], ['#ff0000', '#00be11'])
  return color

pct = .25
start_x = 0.24
start_y = 0.5
h = 0.3
base = 0.01
theta = pct * 180

left_point_x = start_x - base * math.cos(90 - theta)
left_point_y = start_y - base * math.sin(90 - theta)

center_point_x = start_x - h * math.cos(theta)
center_point_y = start_y + h * math.sin(theta)

right_point_x = start_x + base * math.sin(theta)
right_point_y = start_y + base * math.cos(theta)

offset = 50

df.columns = [c.upper() for c in df.columns]
df['PRIOR_VAL'] = df['VAL'].shift(1)
df = df.fillna(0)

base_chart = {
    "values": [offset] + [arc(offset, row['PRIOR_VAL'], row['VAL']) for idx, row in df.iterrows()],
    "labels": [' '] + [row['STAGE'] for idx, row in df.iterrows()],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": ['white'] + [color(row['VAL']) for idx, row in df.iterrows()],
        "line": {
            "width": 1
        }
    },
    "name": "Gauge",
    "hole": .3,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "textinfo": "label",
    "textposition": "inside",
    "hoverinfo": "none"
}

current_val = df['CURRENT_VAL'].max()

layout = {
    'xaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'shapes': [
        {
            'type': 'path',
            'path': f'M {left_point_x} {left_point_y} L {center_point_x} {center_point_y} L {right_point_x} {right_point_y} Z',
            'fillcolor': 'rgba(44, 160, 101, 0.5)',
            'line': {
                'width': 0.5
            },
            'xref': 'paper',
            'yref': 'paper'
        }
    ],
#     'annotations': [
#         {
#             'xref': 'paper',
#             'yref': 'paper',
#             'x': 0.23,
#             'y': 0.45,
#             'text': '50',
#             'showarrow': False
#         }
#     ]
}
fig = dict(data=[base_chart], layout=layout)

# Use Periscope to visualize a dataframe by passing the data to periscope.output()
periscope.plotly(fig)
