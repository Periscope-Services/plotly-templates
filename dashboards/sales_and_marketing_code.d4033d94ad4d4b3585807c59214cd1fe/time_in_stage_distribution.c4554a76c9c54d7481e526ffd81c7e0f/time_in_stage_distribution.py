# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()

counts = df["STAGE_NAME"].value_counts()
print counts.tolist()
print(counts.size)

def null_text():
  fig, ax = plt.subplots(figsize = (10,5))
  ax.axis('off')
  return ax.text(x = 0.5,
                   y = 0.5,
                   s = 'No Opportunities...',
                   color = '#cbd0d8',
                   family = 'sans-serif',
                   fontsize = 25,
                   fontweight = 450,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')
  
def distribute(df):
  counts = df["STAGE_NAME"].value_counts()
  if counts.size==0:
    return null_text()
  df["Stage Name"] = df["STAGE_NAME"]
  df["Number of Days in Stage"] = df["DIFFERENCE"].astype(int)
  # myplot = sns.stripplot(x="STAGE_NAME", y="Number of Days in Stage",data=df, palette="PuBu", size=1, alpha = .25)
  # myplot = sns.violinplot(x="STAGE_NAME", y="Number of Days in Stage", data=df, jitter=False, scale="area", width=2, palette="PuBu")
  fig, ax = plt.subplots(figsize = (8,6))
  myplot = sns.swarmplot(x="Stage Name", y="Number of Days in Stage",data=df, palette=cm.Blues(np.arange(10)/10.+0.2) , order=counts.index)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  spine_color = 'gray'
  for side in ax.spines.keys():  # 'top', 'bottom', 'left', 'right'
    ax.spines[side].set_color(spine_color)
    ax.set_ylabel('Number of Days in Stage', color=spine_color)
    ax.set_xlabel('Stage Name', color = spine_color)
    ax.tick_params(labelcolor=spine_color)
    plt.xticks(rotation=45)
    plt.ylim(0)
    plt.tight_layout()
    plt.figure(figsize=(20,20))
    
  return myplot
  
periscope.output(distribute(df))
