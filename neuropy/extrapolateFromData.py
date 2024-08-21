import multiprocessing
import numpy as np
import argparse
import tempfile
import os
import subprocess
import shlex
from enum import Enum
import navis as nv
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.linalg import lu
from datetime import datetime

TIME_STEP = 5e-5

def extrapolate(i, j, numExtraps, uCurr, slope, timeStep):
    uApprox = uCurr + (slope * (timeStep / numExtraps) * j)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uApprox, vmin=-0.010, vmax=0.05, palette="coolwarm")
    plt.savefig('outputs/frame{0}.png'.format(numExtraps*i + j))
    plt.close()

    return

def start():
    parser = argparse.ArgumentParser(
        prog='extrapolateFromData',
        description='Generates Video of extrapolation from data using ffmpeg'
    )
    parser.add_argument('-d', '--data', default='data/output.txt')
    parser.add_argument('-m', '--morphology', default='data/test.swc')
    parser.add_argument('-f', '--fps', type=int, default=1)
    parser.add_argument('-e', '--extrapolation-rate', type=int, default=0)
    parser.add_argument('-j', '--jump', action="store_true")
    parser.add_argument('-s', '--skip', help="Flag which determines whether or not to skip every other row in data", action="store_true")
    args = parser.parse_args()
    print(args)
    u = pd.read_csv("data/output.txt", delimiter=",", skiprows=lambda x: (x != 0) and not x % 2, dtype=np.float64)
    print(u)
    n = nv.read_swc("data/test.swc")

    i = 0
    uPrev = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        print(tmpdir)
        for index, row in u.iterrows():
            uCurr = row.to_numpy()
            if i == 0:
                uPrev = uCurr
            if i % 100 == 0:
                print(index)

            # create approx slope
            slope = (uCurr - uPrev) / TIME_STEP

            fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uCurr, vmin=-0.010, vmax=0.05, palette="coolwarm")
            plt.savefig(f'{tmpdir}/frame{i}.png')
            plt.close()

            # numExtraps = 50
            # for j in range(numExtraps):
            #     jobs = []
            #     p = multiprocessing.Process(target= extrapolate, args = (i, j, numExtraps, uCurr, slope, TIME_STEP))
            #     jobs.append(p)
            #     p.start()
            # p.join()


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
            command = shlex.split(f"ls -lah {tmpdir}")
            subprocess.run(command)

        # Run ffmpeg from python
        print("running ffmpeg")
        fname = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        command = shlex.split(f"ffmpeg -framerate 1 -i '{tmpdir}/frame%d.png' outputs/{fname}.mp4")
        subprocess.run(command)
        print("ffmpeg complete")



if __name__ == "__main__":
    start()

# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
