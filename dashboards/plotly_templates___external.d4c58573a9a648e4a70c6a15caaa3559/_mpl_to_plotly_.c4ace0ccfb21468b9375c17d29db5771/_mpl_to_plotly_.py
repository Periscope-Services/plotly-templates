import pprint
import numpy as np

# Matplotlib
import matplotlib.pyplot as plt

# Plotly
import plotly.plotly as py
import plotly.tools as tls
## Generating the data..
x =  np.linspace(np.pi, 3*np.pi, 1000)
sinx = np.sin(x)
logx = np.log(x)
# Creating the matplotlib graph..
mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)
ax.plot(x, sinx)
ax.set_title('A Sine Curve')

# periscope.output(mpl_fig)

plotly_fig = tls.mpl_to_plotly(mpl_fig)
periscope.plotly(plotly_fig)