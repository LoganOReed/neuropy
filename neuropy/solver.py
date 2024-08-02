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

def normalizeSWC(filename):
    n = nv.read_swc(filename)



class Solver:
    """Class for Solver"""
    def __init__(self, filename ):
        super(Solver, self).__init__()
        self.filename = filename
        self.neuron = nv.read_swc("data/Green_19weeks_Neuron4.CNG.swc")
        # NOTE: This is required for setTargetTimeStep
        # since "excessively" small edges mess things up
        nv.resample_skeleton(self.neuron, resample_to=3.0,inplace=True)

        # get euclidean distances between node and its parent
        # Get nodes but remove the root (has no parent)
        nodes = self.neuron.nodes[self.neuron.nodes.parent_id > 0]
        # Get the x/y/z coordinates of all nodes (except root)
        node_locs = nodes[['x', 'y', 'z']].values
        # For each node, get its parent's location
        parent_locs = self.neuron.nodes.set_index('node_id').loc[nodes.parent_id.values, ['x', 'y', 'z']].values
        # Calculate Euclidian distances
        self.distances = np.sqrt(np.sum((node_locs - parent_locs)**2, axis=1))
        # Same as InitializeNeuronCell
        # self.temp_u = np.array(self.neuron.nodes)
        self.u = [np.full(self.neuron.nodes['node_id'].size, 0.0),np.full(self.neuron.nodes['node_id'].size, 0.0)]
        self.u_active = self.u[-1]
        self.m = np.full(self.neuron.nodes['node_id'].size, Consts.MI.value)
        self.m_pre = self.m
        self.n = np.full(self.neuron.nodes['node_id'].size, Consts.NI.value)
        self.n_pre = self.n
        self.h = np.full(self.neuron.nodes['node_id'].size, Consts.HI.value)
        self.h_pre = self.h
        self.isyn = np.full(self.neuron.nodes['node_id'].size, 0.0)
        self.r = np.full(self.neuron.nodes['node_id'].size, 0.0)
        self.temp_state = np.full(self.neuron.nodes['node_id'].size, 0.0)
        self.time_step = self.setTargetTimeStep()

    def setTargetTimeStep(self):
        dtmax = 50e-6
        scf = 1e-6
        gll = Consts.GL.value
        if gll == 0.0:
            gll = 1.0
        upper_bound = Consts.CAP.value * self.neuron.sampling_resolution * scf * np.sqrt(Consts.RES.value / (gll * np.min(self.distances) * scf ))
        return min(upper_bound, dtmax)

    def reactF(self, u_active, n, m, h):
        return 0.1
        

    # TODO:
    def solveStep(self, curStep):
        self.u_active = (4.0 / 3.0) * np.dot(self.u_active,self.r)
        self.r = self.r + (((4.0/3.0) * self.time_step) * self.reactF(self.u_active, self.n, self.m, self.h))
        self.r = self.r + ((-1.0/3.0) * self.u[-2])
        self.r = self.r + (((-2.0/3.0) * self.time_step) * self.reactF(self.u[-2], self.n_pre, self.m_pre, self.h_pre))
        self.r = self.r + self.isyn
        self.isyn = self.isyn * 0.0
        print(self.r)
        return

    
    def print(self):
        # print(self.neuron.nodes['node_id'].size)
        print(self.u)
        print(self.m)
        print(self.n)
        print(self.r)
        print(self.neuron.nodes)
        print(self.neuron.segments)
        print(self.distances)
        print(nv.segment_analysis(self.neuron))
        # same as TargetEdgeLength in cs code
        print(self.neuron.sampling_resolution)
        print(self.time_step)








if __name__ == "__main__":

    n = nv.read_swc("data/Green_19weeks_Neuron4.CNG.swc")


    

    # for i in range(0, 255, 1):
    #    # Change rotation
    #
    #    fig, ax = nv.plot2d(n, method='2d', view=('x', 'y'), color=(0,i,0))
    #
    #    # Save each incremental rotation as frame
    #    plt.savefig('outputs/frame{0}.png'.format(i))
    #    plt.close()
    #    # plt.show()

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
    s = Solver("data/Green_19weeks_Neuron4.CNG.swc")
    s.print()


    for curStep in range(totalSteps):
        s.solveStep(curStep)

    print(totalSteps)

