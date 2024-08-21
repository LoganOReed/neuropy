import multiprocessing
import time
from alive_progress import alive_bar
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


def extrapolate(n, i, j, numExtraps, dir, uCurr, uProjected):
    uInterpolate = uCurr + (uProjected - uCurr) * (j / numExtraps)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uInterpolate, vmin=-0.010, vmax=0.05, palette="coolwarm")
    plt.savefig(f'{dir}/frame{numExtraps*i + j}.png')
    plt.close()

    return

def start():

    TIME_STEP = 5e-5
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
    parser.add_argument('-j', '--jump', help="Flag which determines whether the extrapolation uses previous guess as the starting point", action="store_true")
    parser.add_argument('-p', '--preview', help="Flag to automatically launch the video", action="store_true")
    parser.add_argument('-s', '--skip', help="Determines how many data points are used. E.g. 2 would mean half, 3 would mean a third.", type=int, default=1)
    parser.add_argument('-c', '--color', help="The color palette, needs to be a name of a matplotlib colormap", default="coolwarm")

    args = parser.parse_args()
    print(args)
    # Generate name and read proper file


    u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", skiprows=lambda x: x % args.skip != 0, dtype=np.float64)
    n = nv.read_swc(f"data/{args.morphology}.swc")

    i = 0
    uPrev = 0
    uApprox = 0
    print(u.shape[0])
    numIters = u.shape[0] 
    with tempfile.TemporaryDirectory() as tmpdir:
        with alive_bar(numIters) as bar:
            for index, row in u.iterrows():
                uCurr = row.to_numpy()
                if i == 0:
                    uPrev = uCurr
                    uApprox = uCurr

                # create approx slope

                if args.extrapolation_rate == 0:
                    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uCurr, vmin=-0.010, vmax=0.05, palette=args.color)
                    plt.savefig(f'{tmpdir}/frame{i}.png')
                    plt.close()
                else:
                    # uProjected is calculated using a simplified form of the line formula for uCurr and uPrev
                    uProjected = 2*uCurr - uPrev
                    for j in range(args.extrapolation_rate):
                        jobs = []
                        if args.jump:
                            p = multiprocessing.Process(target= extrapolate, args = (n, i, j, args.extrapolation_rate, tmpdir, uCurr, uProjected))
                        else:
                            p = multiprocessing.Process(target= extrapolate, args = (n, i, j, args.extrapolation_rate, tmpdir, uApprox, uProjected))
                        jobs.append(p)
                        p.start()
                    p.join()


                uApprox = 2*uCurr - uPrev
                uPrev = row.to_numpy()
                i += 1
                bar()


        # Run ffmpeg from python
        if args.skip != 1:
            if args.jump:
                name = f"{args.data}_{args.fps}x{args.extrapolation_rate}s{args.skip}j"
            else:
                name = f"{args.data}_{args.fps}x{args.extrapolation_rate}s{args.skip}"
        else:
            if args.jump:
                name = f"{args.data}_{args.fps}x{args.extrapolation_rate}j"
            else:
                name = f"{args.data}_{args.fps}x{args.extrapolation_rate}"
        fname = name + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        if args.extrapolation_rate == 0:
            command = shlex.split(f"ffmpeg -framerate {args.fps} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        else:
            command = shlex.split(f"ffmpeg -framerate {args.extrapolation_rate} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        if args.preview:
            command = shlex.split(f"mpv outputs/{fname}.mp4")
            subprocess.run(command)
        else:
            print(f"Wrote to outputs/{fname}.mp4")




if __name__ == "__main__":
    start()

# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
