# import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.path as Path
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.gridspec import GridSpec

### HELPER FUNCTION
# prettify numbers
def prettify_num(num):
  pretty_num = ''
  if abs(num) < 10**3:
    pretty_num = str(num)
  elif abs(num) < 10**6:
    pretty_num = str(round(1.0*num/10**3,1)) + 'K'
  elif abs(num) < 10**9:
    pretty_num = str(round(1.0*num/10**6,1)) + 'M'
  else:
    pretty_num = str(round(1.0*num/10**9,1)) + 'B'
  return pretty_num


df['COST'] = df['COST'].astype(int)
df['LEADS'] = df['LEADS'].astype(int)
df['PIPELINE'] = df['PIPELINE'].astype(int)
df['COST_RANK'] = df['COST_RANK'].astype(int)
df['LEADS_RANK'] = df['LEADS_RANK'].astype(int)
df['PIPELINE_RANK'] = df['PIPELINE_RANK'].astype(int)

# set up the base of the canvas
fig, axes = plt.subplots(figsize = (32,30), nrows = 1, ncols = 2, sharey= True)
# fig.subplots_adjust(left=0.05, bottom=0, right=1, top=1, wspace=0, hspace=0)

# chart title
fig.suptitle("Channel Performance", color = 'gray', fontsize=60)

# colors 
names = df['CHANNEL'].unique().tolist()
colors = ["#6fb8ff", "#ff7555", "#59cec5", "#8849a5","#6b5b95", "#feb236", 
          "#d64161", "#405d27", "#ff7b25", "#034f84", "#80ced6", "#ffef96",
         "#618685", "#82b74b", "#eca1a6", "#D4318C", "#DC143C", "#DC8909"]  
color_assignment = [colors[names.index(name)%len(colors)] for name in names]
color_dict = dict(zip(names, color_assignment))




# ladder plot
def make_ladders(ax, data, piece, rank1, rank2, labs, labels, title, start = 0):
    # plot
    ax.axis('off')
    
    # key data structures
    df_dict = data.to_dict('records')
    df_dict = sorted(df_dict, key=lambda k: k['COST'], reverse = True) 
#     names = data[labs].unique().tolist()
    num_names = len(names)
    num_names = len(names)

    # key visual variables 
    ladder_width = 0.11
    ladder_height = 0.88
    ladder_base_color = 'paleturquoise'
    
    lab_pos_x = start
    arr_pox_x = start + 0.1
    rank1_pos_x = lab_pos_x + 0.01
    rank2_pos_x = rank1_pos_x + ladder_width

    name_padding_h = 0.01
    name_padding_v = 0.05
    arr_padding_v = 0.015
    
    name_font_size = 28
    num_font_size = 23
    

    # draw the shapes
    for i, r in enumerate(df_dict):
        # rep vars
        rep_color = color_dict[r[labs]]
        rep_y = ladder_height - ladder_height/num_names*(r[rank1] - 1) - name_padding_v
#         y = ladder_height - ladder_height/num_names*i - name_padding_v
        
        # the name labels
        ax.text(x = lab_pos_x,
           y = rep_y,
           s = r[labs],
           family = 'sans-serif',
           fontsize = name_font_size,
           color = 'gray',
           horizontalalignment = 'right',
           verticalalignment = 'center')
        
        # the arr labels
        ax.text(x = rank1_pos_x + 0.008,
           y = rep_y,
           s = '$' + prettify_num(r['COST']),
           family = 'sans-serif',
           fontsize = num_font_size,
#            color = '#b1b5bc',
           alpha = 0.8,
           color = 'gray',
           horizontalalignment = 'left',
           verticalalignment = 'center')
        
       # the acv labels
        ax.text(x = rank2_pos_x - 0.008,
           y = ladder_height - ladder_height/num_names*(r[rank2] - 1) - name_padding_v,
           s = prettify_num(r['LEADS']) if piece=='leads' else '$' + prettify_num(r['PIPELINE']),
           family = 'sans-serif',
           fontsize = num_font_size,
#            color = '#b1b5bc',
           alpha = 0.8,
           color = 'gray',
           horizontalalignment = 'right',
           verticalalignment = 'center')
        
        # the left circles
        ax.text(x = rank1_pos_x,
                   y = rep_y,
                   s = '⬤',
                   family = 'sans-serif',
                   fontsize = 40,
    #                alpha = 0.5 if r['position'] in (2,3) else 1,
                   color = rep_color,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')
        
         # the left inner circles
        ax.text(x = rank1_pos_x + 0.032,
                   y = rep_y,
                   s = '⬤',
                   family = 'sans-serif',
                   fontsize = 10,
    #                alpha = 0.5 if r['position'] in (2,3) else 1,
                   color = rep_color,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')
        
        # the right circles
        ax.text(x = rank2_pos_x,
                   y = ladder_height - ladder_height/num_names*(r[rank2] - 1) - name_padding_v,
                   s = '⬤',
                   family = 'sans-serif',
                   fontsize = 40,
    #                alpha = 0.5 if r['position'] in (2,3) else 1,
                   color = rep_color,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')
        
        # the right inner circles
        ax.text(x = rank2_pos_x - 0.028,
                   y = ladder_height - ladder_height/num_names*(r[rank2] - 1) - name_padding_v,
                   s = '⬤',
                   family = 'sans-serif',
                   fontsize = 10,
    #                alpha = 0.5 if r['position'] in (2,3) else 1,
                   color = rep_color,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')
        
        # the ranks on the left circles
        ax.text(x = rank1_pos_x,
           y = rep_y,
           s = r[rank1],
           family = 'sans-serif',
           fontsize = 18,
           fontweight = 'bold',
           color = 'white',
           horizontalalignment = 'center',
           verticalalignment = 'center')
        
        # the ranks on the right circles
        ax.text(x = rank2_pos_x,
           y = ladder_height - ladder_height/num_names*(r[rank2] - 1) - name_padding_v,
           s = r[rank2],
           family = 'sans-serif',
           fontsize = 18,
           fontweight = 'bold',
           color = 'white',
           horizontalalignment = 'center',
           verticalalignment = 'center')
        
        # the lines
        r1 = r[rank1]
        r2 = r[rank2]
        y1 = ladder_height - ladder_height/num_names*(r1 - 1) - name_padding_v
        y2 = ladder_height - ladder_height/num_names*(r2 - 1) - name_padding_v

        li = ax.plot([rank1_pos_x + 0.032, rank2_pos_x - 0.028], 
                           [y1, y2], 
#                            transform=fig.transFigure, 
#                            figure=ax, 
                           color = rep_color, 
                           alpha = 0.35, 
                           linewidth = 3)
#         ax.lines.extend([li])
    
    
    # create the header labels
    for i in range(2):
        ax.text(x = rank1_pos_x if i == 0 else rank2_pos_x,
               y = ladder_height,
               s = labels[i],
               family = 'sans-serif',
               fontsize = 24,
               color = 'gray',
               fontweight='bold',
               horizontalalignment = 'center',
               verticalalignment = 'center')
        
    #title
    ax.text(x = rank1_pos_x + (rank2_pos_x - rank1_pos_x)/2,
                y = ladder_height + 0.035,
                s = title,
                family = 'sans-serif',
                fontsize = 30,
                color = 'gray',
                horizontalalignment = 'center',
                verticalalignment = 'center')
    return ax
    

make_ladders(ax = axes[0], data = df, piece = 'leads', rank1 = 'COST_RANK', rank2 = 'LEADS_RANK', labs = 'CHANNEL', labels = ['COST', 'LEADS'], title = 'Leads Generated', start = 0)
make_ladders(ax = axes[1], data = df, piece = 'pipeline', rank1 = 'COST_RANK', rank2 = 'PIPELINE_RANK', labs = 'CHANNEL', labels = ['COST', 'PIPELINE'], title = 'Pipeline Generated', start = 0)
fig.subplots_adjust(left=0.25, wspace=3)

periscope.output(fig)