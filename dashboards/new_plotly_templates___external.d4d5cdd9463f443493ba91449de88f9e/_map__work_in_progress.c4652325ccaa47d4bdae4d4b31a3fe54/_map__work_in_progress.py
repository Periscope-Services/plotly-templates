from plotly.offline import init_notebook_mode, iplot
import pandas as pd

df.columns = [c.upper() for c in df.columns]

series_col = [c for c in df.columns if c.startswith('S')][0]
lat_col = 'LATITUDE'
lon_col = 'LONGITUDE'
unique_series = df.groupby(series_col).size().reset_index()[series_col]

data = []
steps = []
for idx, series in enumerate(unique_series):
  data.append(
    dict(
      lat = df[df[series_col] == series][lat_col],
      lon = df[df[series_col] == series][lon_col],
      type = 'scattergeo',
      locationmode = 'USA-states',
      marker = dict(
        size = 2
      ),
      visible = True if idx == 0 else False
    )
  )
  steps.append(
    dict(
      label = str(series),
      method = 'restyle',
      args = [
        dict(
          visible = [True if s == series else False for s in unique_series]
        )
      ]
    )
  )

layout = dict(
  geo = dict(
    scope = 'usa',
    projection=dict(type='albers usa'),
    showland = True,
    landcolor = "rgb(250, 250, 250)",
    subunitcolor = "rgb(217, 217, 217)",
    countrycolor = "rgb(217, 217, 217)",
    countrywidth = 0.5,
    subunitwidth = 0.5
  ),
  margin=dict(
                t=20,
                b=50,
                l=10,
                r=10
              ),
  sliders = [
    dict(
      active=0,
      steps=steps,
    )
  ] 
)

fig = dict(data=data, layout=layout)
periscope.plotly(fig)