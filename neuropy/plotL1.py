import multiprocessing
from alive_progress import alive_bar
import numpy as np
from numpy import linalg as LA
import argparse
import tempfile
import subprocess
import shlex
import navis as nv
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def extrapolate(n, i, j, numExtraps, numSkip, isJump, dir, uCurr, uProjected, data):
    uInterpolate = uCurr + (uProjected - uCurr) * (j / numExtraps)
    try:
        uActual = pd.read_csv(f"data/{data}.csv", delimiter=",", header=None, skiprows=lambda x:x != i*numExtraps + j , dtype=np.float64)
        l1 = LA.norm(uActual-uInterpolate, 1)
    except pd.errors.EmptyDataError:
        l1 = 0
    # ax.annotate(f"{numExtraps*i + j}", 
    #             xy=(1,3),
    #             xytext=(1, 3)
    #             )
    # ax.text(-0.9,0.3, "frame: 1234567890", ha='right')

    return l1

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

    # u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", header=None, skiprows=lambda x:x % args.skip != 0, dtype=np.float64)
    u = pd.read_csv(f"data/{args.data}.csv", delimiter=",", header=None, dtype=np.float64)
    n = nv.read_swc(f"data/{args.morphology}.swc")

    norms = []
    i = 0
    uPrev = 0
    uApprox = 0
    numIters = u.query(f'index % {args.skip} == 0').shape[0] 
    with tempfile.TemporaryDirectory() as tmpdir:
        with alive_bar(numIters) as bar:
            bar.title(name)
            for index, row in u.query(f'index % {args.skip} == 0').iterrows():
                # print(index)
                uCurr = row.to_numpy()
                if i == 0:
                    uPrev = uCurr
                    uApprox = uCurr

                if args.extrapolation_rate == 0:
                    uActual = pd.read_csv(f"data/{args.data}.csv", delimiter=",", header=None, skiprows=lambda x:x != i*args.skip, dtype=np.float64)

                    l1 = LA.norm(uActual-uCurr, 1)
                    norms = norms + [l1]
                else:
                    # uProjected is calculated using a simplified form of the line formula for uCurr and uPrev
                    uProjected = 2*uCurr - uPrev
                    for j in range(args.extrapolation_rate):
                        if args.jump:
                            norms = norms + [extrapolate(n, i, j, args.extrapolation_rate, args.skip, args.jump, tmpdir, uCurr, uProjected, args.data)]
                        else:
                            norms = norms + [extrapolate(n, i, j, args.extrapolation_rate, args.skip, args.jump, tmpdir, uApprox, uProjected, args.data)]


                uApprox = 2*uCurr - uPrev
                uPrev = row.to_numpy()
                i += 1
                bar()


        # Run ffmpeg from python

        # Uncomment if you want timestamps on the files
        # fname = name + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        # Write data to file to combine plots
        df = pd.DataFrame(norms)
        df.to_csv(f"data/{name}_l1.csv")
        print(df)
        plt.plot(norms)
        plt.show()
        print(f"Wrote to outputs/{name}_l1.png")

        # fname = name
        # if args.extrapolation_rate == 0:
        #     command = shlex.split(f"ffmpeg -y -framerate {args.fps} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        # else:
        #     command = shlex.split(f"ffmpeg -y -framerate {args.extrapolation_rate} -i '{tmpdir}/frame%d.png' -r {args.target_fps} outputs/{fname}.mp4")
        # subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        #
        # if args.preview:
        #     command = shlex.split(f"mpv outputs/{fname}.mp4")
        #     subprocess.run(command)
        # else:
        #     print(f"Wrote to outputs/{fname}.mp4")
        #



if __name__ == "__main__":
    data = pd.read_csv("data/endpointFull_10s10e_l1.csv")
    data2 = pd.read_csv("data/endpointFull_10s10ej_l1.csv")
    # data = pd.concat([data,data2])
    plt.rcParams.update({'font.size': 20})
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(range(200),data[:200], 'b', label="Linear Extrapolation without Jumps")
    ax.plot(range(200),data2[:200], 'g', label="Linear Extrapolation with Jumps")
    ax.set_xticks(np.arange(0,200,10))
    ax.grid(which="both", axis='x')
    ax.legend(fontsize=24)
    # plt.title("Linear Extrapolation ", fontsize=24)
    plt.xlabel("Extrapolation Step", fontsize=24)
    plt.ylabel("L1 Norm", fontsize=24)
    plt.show()

    plt.savefig(f'outputs/endpointFull_10s10e_both_l1.png')

# fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
#
# # Save each incremental rotation as frame
# plt.show()
