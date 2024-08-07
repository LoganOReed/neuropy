import numpy as np
from enum import Enum
import navis as nv
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.linalg import lu


u = pd.read_csv("data/output.txt", delimiter=",", dtype=np.float64)
print(u)
n = nv.read_swc("data/test.swc")

i = 0
for index, row in u.iterrows():
    if i % 100 == 0:
        print(index)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=row.to_numpy(), vmin=-0.010, vmax=0.05, palette="coolwarm")
    # Save each incremental rotation as frame
    plt.savefig('outputs/frame{0}.png'.format(i))
    # for j in range(20):
    #     plt.savefig('outputs/frame{0}.png'.format(20*i + j))
    plt.close()
    i += 1


# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
