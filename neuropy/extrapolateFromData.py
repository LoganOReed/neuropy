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

def extrapolate(n, i, j, numExtraps, combinedFps, dir, uCurr, slope, timeStep):
    repeatFrames = combinedFps // numExtraps
    uApprox = uCurr + (slope * (timeStep / numExtraps) * j)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uApprox, vmin=-0.010, vmax=0.05, palette="coolwarm")
    for _ in range(repeatFrames):
        plt.savefig('outputs/frame{0}.png'.format(numExtraps*i + j))
        plt.savefig(f'{dir}/frame{i}.png')
    plt.close()

    return

def start():
    parser = argparse.ArgumentParser(
        prog='extrap',
        description='Generates Video of extrapolation from data using ffmpeg'
    )
    name = ""
    parser.add_argument('-d', '--data', default='center')
    parser.add_argument('-m', '--morphology', default='NeuroVISOR_Green_19weeks_Neuron4')
    parser.add_argument('-f', '--fps', help="The rate the actual data is used in terms of fps", type=int, default=1)
    parser.add_argument('-e', '--extrapolation-rate', type=int, default=0)
    parser.add_argument('--target-fps', help="The fps of the final video, fps and extrap rate should to be divisors", type=int, default=60)
    parser.add_argument('-j', '--jump', action="store_false")
    parser.add_argument('-s', '--skip', help="Flag which determines whether or not to skip every other row in data", action="store_true")
    parser.add_argument('-c', '--color', help="The color palette, needs to be a name of a matplotlib colormap", default="coolwarm")

    args = parser.parse_args()
# 1x0j
    print(args)
    # Generate name and read proper file
    if args.skip:
        if args.jump:
            name = f"{args.data}_{args.fps}x{args.extrapolation_rate}sj"
        else:
            name = f"{args.data}_{args.fps}x{args.extrapolation_rate}s"
        u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", skiprows=lambda x: (x != 0) and not x % 2, dtype=np.float64)
    else:
        if args.jump:
            name = f"{args.data}_{args.fps}x{args.extrapolation_rate}j"
        else:
            name = f"{args.data}_{args.fps}x{args.extrapolation_rate}"
        u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", dtype=np.float64)
    n = nv.read_swc(f"data/{args.morphology}.swc")

    i = 0
    uPrev = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for index, row in u.iterrows():
            uCurr = row.to_numpy()
            if i == 0:
                uPrev = uCurr

            # create approx slope
            slope = (uCurr - uPrev) / TIME_STEP

            if args.extrapolation_rate == 0:
                fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uCurr, vmin=-0.010, vmax=0.05, palette=args.color)
                plt.savefig(f'{tmpdir}/frame{i}.png')
                plt.close()
            else:
                numExtraps = args.extrapolation_rate 
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

        # Run ffmpeg from python
        fname = name + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        if args.extrapolation_rate == 0:
            command = shlex.split(f"ffmpeg -framerate {args.fps} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        else:
            command = shlex.split(f"ffmpeg -framerate {args.extrapolation_rate} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



if __name__ == "__main__":
    start()

# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
