import multiprocessing
import numpy as np
from enum import Enum
import navis as nv
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.linalg import lu

TIME_STEP = 5e-5

def extrapolate(i, j, numExtraps, uCurr, slope, timeStep):
    uApprox = uCurr + (slope * (timeStep / numExtraps) * j)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uApprox, vmin=-0.010, vmax=0.05, palette="coolwarm")
    plt.savefig('outputs/frame{0}.png'.format(numExtraps*i + j))
    plt.close()

    return

if __name__ == "__main__":
    u = pd.read_csv("data/output.txt", delimiter=",", dtype=np.float64)
    print(u)
    n = nv.read_swc("data/test.swc")

    i = 0
    uPrev = 0
    for index, row in u.iterrows():
        uCurr = row.to_numpy()
        if i == 0:
            uPrev = uCurr
        if i % 100 == 0:
            print(index)

        # create approx slope
        slope = (uCurr - uPrev) / TIME_STEP

        # fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uCurr, vmin=-0.010, vmax=0.05, palette="coolwarm")
        # plt.savefig('outputs/frame{0}.png'.format(i))
        # plt.close()

        numExtraps = 50
        for j in range(numExtraps):
            jobs = []
            p = multiprocessing.Process(target= extrapolate, args = (i, j, numExtraps, uCurr, slope, TIME_STEP))
            jobs.append(p)
            p.start()
        p.join()


        # for j in range(30):
        #     uApprox = uCurr + (slope * TIME_STEP * j)
        #     fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uApprox, vmin=-0.010, vmax=0.05, palette="coolwarm")
        #     plt.savefig('outputs/frame{0}.png'.format(30*i + j))
        #     plt.close()

        # Save each incremental rotation as frame
        # for j in range(30):
        #     plt.savefig('outputs/frame{0}.png'.format(30*i + j))
        # plt.close()
        uPrev = row.to_numpy()
        # print(uPrev)
        i += 1


# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
