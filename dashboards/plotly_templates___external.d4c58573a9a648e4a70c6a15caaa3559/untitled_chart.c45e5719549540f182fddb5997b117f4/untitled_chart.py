# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go

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

offset = 50

df.columns = [c.upper() for c in df.columns]
df['PRIOR_VAL'] = df['VAL'].shift(1)
df = df.fillna(0)

base_chart = {
    "values": [offset] + [arc(offset, row['PRIOR_VAL'], row['VAL']) for idx, row in df.iterrows()],
    "labels": [''] + [row['STAGE'] for idx, row in df.iterrows()],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": ['white'] + [color(row['VAL']) for idx, row in df.iterrows()],
        "line": {
            "width": 1
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"
}

fig = dict(data=[base_chart])

# Use Periscope to visualize a dataframe by passing the data to periscope.output()
periscope.plotly(fig)
