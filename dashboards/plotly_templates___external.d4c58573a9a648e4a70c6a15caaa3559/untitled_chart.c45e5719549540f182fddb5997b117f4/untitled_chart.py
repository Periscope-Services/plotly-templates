# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
import plotly.plotly as py
import plotly.graph_objs as go

def arc(offset, start, end):
  return 1.0 * (end - start) / 100 * offset

offset = 50

df.columns = [c.upper() for c in df.columns]
df['PRIOR_VAL'] = df['VAL'].shift(1)
df = df.fillna(0)
print([offset] + [arc(offset, row['PRIOR_VAL'], row['VAL']) for idx, row in df.iterrows()])

base_chart = {
    "values": [offset] + [arc(offset, row['PRIOR_VAL'], row['VAL']) for idx, row in df.iterrows()],
    "labels": ["-", "0", "20", "40", "60", "80", "100"],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)'
        ],
        "line": {
            "width": 1
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 108,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"
}

# Use Periscope to visualize a dataframe by passing the data to periscope.output()
periscope.output(df)
