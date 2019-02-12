# SQL output is imported as a dataframe variable called 'df'
import pandas as pd 
from random import shuffle
from datetime import timedelta

df.columns = [c.upper() for c in df.columns]
current_date = df['CURRENT_DATE'].iloc[0]

cookies = ['Thin Mints', 'Samoas' ,'Trefoils', 'Do-si-dos', 'Tagalongs']
vals = []

for i in range(0,30):
  date = current_date - timedelta(days=i)
  shuffle(cookies)
  for k in range(0, len(cookies)):
    vals.append({
      'date': date,
      'cookie': cookies[k],
      'rank': k + 1
    })

# Use Periscope to materialize a dataframe by passing the data to periscope.materialize()
periscope.materialize(pd.DataFrame(vals))
