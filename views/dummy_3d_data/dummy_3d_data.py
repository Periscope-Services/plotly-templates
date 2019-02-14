import pandas as pd
import numpy as np

x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 2000).transpose()

df = pd.DataFrame({'x':x, 'y': y, 'z': z})
periscope.materialize(df)