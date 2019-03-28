# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go

df.columns = [c.lower() for c in df.columns]
df['y'] = pd.to_numeric(df['y'])



# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.table(df)
