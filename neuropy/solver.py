import numpy as np
from enum import Enum
import navis as nv
import pandas as pd
import matplotlib.pyplot as plt

class Consts(Enum):
    VCLAMP = 0.05
    RES = 3.0
    CAP = 0.01
    GK = 5.0
    GNA = 50.0
    GL = 0.0 #NOTE: Ask Seibold about this
    ENA = 0.05
    EL = -0.07
    NI = 0.0376969
    MI = 0.0147567
    HI = 0.9959410



# initializes the solution vectors
# U, M, N, H
def preSolve():
    #build arrays
    u = np.zeros(1)





if __name__ == "__main__":

    n = nv.read_swc("data/Green_19weeks_Neuron4.CNG.swc")
    

    for i in range(0, 360, 10):
       # Change rotation
       
       fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), color=(0,i,0))
       
       # Save each incremental rotation as frame
       plt.savefig('outputs/frame_{0}.png'.format(i))
       plt.close()
       # plt.show()

    #
    # Start of solving loop logic
    #
    t_pde = 0.008 * 1e-3
    t_sim = 0.01
    t_vis = 0.02
    endTime = 1.0
    totalSteps = (int)(endTime // t_pde)

    # main solving loop

    # preSolve()

    # for curStep in range(totalSteps):
    #     preSolveStep(curStep)
    #     solveStep(curStep)
    #     postSolveStep(curStep)

    # postSolve()
    print(totalSteps)
    print(Consts.VCLAMP.value)

