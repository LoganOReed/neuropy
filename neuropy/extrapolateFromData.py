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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def extrapolate(n, i, j, numExtraps, numSkip, isJump, dir, uCurr, uProjected):
    uInterpolate = uCurr + (uProjected - uCurr) * (j / numExtraps)
    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uInterpolate, vmin=-0.010, vmax=0.05, palette="coolwarm")
    axtext = inset_axes(ax, width="30%", height="40%", loc="center left")
    fig.patch.set_visible(False)
    if isJump:
        fig.suptitle(f"Display One in {numSkip} Simulation Data Points, \n{numExtraps} Extrapolations per Data Point (from Data Point)")
    else:
        fig.suptitle(f"Display One in {numSkip} Simulation Data Points, \n{numExtraps} Extrapolations per Data Point (from Extrapolated Point)")

    axtext.axis('off')
    # axtext.tick_params(axis='both', which='both', labelsize='large',
    #            bottom=False, top=False, labelbottom=False,
    #            left=False, right=False, labelleft=False)
    axtext.text(0,0.9, f"Simulation: {i+1}", ha='right', fontsize="large")
    axtext.text(0,0.8, f"Extrapolation: {j+1}", ha='right', fontsize="large")
    axtext.text(0,0.7, f"Extrapolation Total: {numExtraps*i+j+1}", ha='right', fontsize="large")
    # ax.annotate(f"{numExtraps*i + j}", 
    #             xy=(1,3),
    #             xytext=(1, 3)
    #             )
    # ax.text(-0.9,0.3, "frame: 1234567890", ha='right')
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
#center_2s30ej
    if args.skip != 1:
        if args.jump:
            name = f"{args.data}_{args.skip}s{args.extrapolation_rate}ej"
        else:
            name = f"{args.data}_{args.skip}s{args.extrapolation_rate}e"
    else:
        if args.jump:
            name = f"{args.data}_{args.fps}f{args.extrapolation_rate}ej"
        else:
            name = f"{args.data}_{args.fps}f{args.extrapolation_rate}e"

    u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", skiprows=lambda x: x % args.skip != 0, dtype=np.float64)
    n = nv.read_swc(f"data/{args.morphology}.swc")

    i = 0
    uPrev = 0
    uApprox = 0
    numIters = u.shape[0] 
    with tempfile.TemporaryDirectory() as tmpdir:
        with alive_bar(numIters) as bar:
            bar.title(name)
            for index, row in u.iterrows():
                uCurr = row.to_numpy()
                if i == 0:
                    uPrev = uCurr
                    uApprox = uCurr
                if i == 1:
                    uApprox = uCurr

                # create approx slope

                if args.extrapolation_rate == 0:
                    fig, ax = nv.plot2d(n, linewidth=3, method='2d', view=('x', 'y'), color_by=uCurr, vmin=-0.010, vmax=0.05, palette=args.color)

                    axtext = inset_axes(ax, width="30%", height="40%", loc="center left")
                    fig.patch.set_visible(False)
                    fig.suptitle(f"Display One in {args.skip} Simulation Data Points, \n{args.extrapolation_rate} Extrapolations per Data Point (from Data Point)")
                    axtext.axis('off')
                    axtext.text(0,0.9, f"Simulation: {i+1}", ha='right', fontsize="large")
                    plt.savefig(f'{tmpdir}/frame{i}.png')
                    plt.close()
                else:
                    # uProjected is calculated using a simplified form of the line formula for uCurr and uPrev
                    uProjected = 2*uCurr - uPrev
                    for j in range(args.extrapolation_rate):
                        jobs = []
                        if args.jump:
                            p = multiprocessing.Process(target= extrapolate, args = (n, i, j, args.extrapolation_rate, args.skip, args.jump, tmpdir, uCurr, uProjected))
                        else:
                            p = multiprocessing.Process(target= extrapolate, args = (n, i, j, args.extrapolation_rate, args.skip, args.jump, tmpdir, uApprox, uProjected))
                        jobs.append(p)
                        p.start()
                    p.join()


                uApprox = 2*uCurr - uPrev
                uPrev = row.to_numpy()
                i += 1
                bar()


        # Run ffmpeg from python

        # Uncomment if you want timestamps on the files
        # fname = name + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        fname = name
        if args.extrapolation_rate == 0:
            command = shlex.split(f"ffmpeg -y -framerate {args.fps} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        else:
            command = shlex.split(f"ffmpeg -y -framerate {args.extrapolation_rate} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
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
