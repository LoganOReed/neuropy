import numpy as np
from enum import Enum
import navis as nv
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import lu_factor, lu_solve
import collections

class Consts(Enum):
    VCLAMP = 0.05
    RES = 3.0
    CAP = 0.01
    GK = 5.0
    GNA = 50.0
    GL = 0.0 #NOTE: Ask Seibold about this
    ENA = 0.05
    EL = -0.07
    EK = -0.09
    NI = 0.0376969
    MI = 0.0147567
    HI = 0.9959410
    SCF = 1e-6


class Solver:
    """Class for Solver"""
    def __init__(self, filename ):
        super(Solver, self).__init__()
        self.filename = filename
        self.neuron = nv.read_swc("data/Green_19weeks_Neuron4.CNG.swc")
        # NOTE: This is required for setTargetTimeStep
        # since "excessively" small edges mess things up
        nv.resample_skeleton(self.neuron, resample_to=3.0,inplace=True)
        # self.neighbors = nv.neuron2nx(self.neuron).adj
        # self.neighbors = [[] for _ in range(self.neuron.nodes['node_id'].size)]
        self.neighbors = collections.defaultdict(list)
        # print(len(self.neighbors))
        for e in self.neuron.edges:
            # print(self.neighbors[e[0]])
            self.neighbors[e[0]].append(e[1])
            self.neighbors[e[-1]].append(e[0])
        # print(self.neighbors)

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
        self.u = [np.full(self.neuron.nodes['node_id'].size, 0.0).astype("float64"),np.full(self.neuron.nodes['node_id'].size, 0.0).astype("float64")]
        self.m = np.full(self.neuron.nodes['node_id'].size, Consts.MI.value).astype("float64")
        self.m_pre = self.m
        self.n = np.full(self.neuron.nodes['node_id'].size, Consts.NI.value).astype("float64")
        self.n_pre = self.n
        self.h = np.full(self.neuron.nodes['node_id'].size, Consts.HI.value).astype("float64")
        self.h_pre = self.h
        self.isyn = np.full(self.neuron.nodes['node_id'].size, 0.0).astype("float64")
        self.r = np.full(self.neuron.nodes['node_id'].size, 0.0).astype("float64")
        self.time_step = self.setTargetTimeStep()
        self.lhs, self.rhs = self.makeSparseStencils()
        self.lu, self.piv = lu_factor(self.lhs)
        self.uMin = -99999.9
        self.uMax = 999999.999

    def setTargetTimeStep(self):
        dtmax = 50e-6
        gll = Consts.GL.value
        if gll == 0.0:
            gll = 1.0
        upper_bound = Consts.CAP.value * self.neuron.sampling_resolution * Consts.SCF.value * np.sqrt(Consts.RES.value / (gll * np.min(self.distances) * Consts.SCF.value ))
        self.time_step = min(upper_bound, dtmax)
        return min(upper_bound, dtmax)

    def reactF(self, V, NN, MM, HH):
        output = np.zeros(len(V))
        prod = np.power(NN, 4.0)
        prod = np.multiply((np.subtract(V, Consts.EK.value)),prod)
        output = np.add(np.multiply(prod, Consts.GK.value), output)

        prod = np.power(MM, 3.0)
        prod = np.multiply(HH, prod)
        prod = np.multiply((np.subtract(V, Consts.ENA.value)),prod)
        output = np.add(np.multiply(prod, Consts.GNA.value), output)
        output = np.add(np.multiply(np.subtract(V, Consts.EL.value),Consts.GL.value), output)
        output = np.multiply(-1.0 / Consts.CAP.value, output)

        return output 

    def makeSparseStencils(self):
        lhs = self.neuron.geodesic_matrix.astype('float64')
        for col in lhs.columns:
            lhs[col].values[:] = 0.0
        lhs = lhs.astype('float64')
        rhs = self.neuron.geodesic_matrix.astype('float64')
        for col in rhs.columns:
            rhs[col].values[:] = 0.0
        rhs = rhs.astype('float64')

        # lhs = np.zeros((self.neuron.nodes['node_id'].size,self.neuron.nodes['node_id'].size))
        # rhs = np.zeros((self.neuron.nodes['node_id'].size,self.neuron.nodes['node_id'].size))

        # for i in range(self.neuron.nodes['node_id'].size):

        # To get distance between two values
        # print(self.neuron.geodesic_matrix.at[self.neuron.edges[i][0], self.neuron.edges[i][1]])


        # neighbors = [[] for _ in range(self.neuron.nodes['node_id'].size)]
        # for e in self.neuron.edges:
        #     neighbors[e[0]].append(e[1])
        #     neighbors[e[1]].append(e[0])
        for n in self.neuron.nodes['node_id']:
            edgeLengths = []
            sumRecip = 0.0
            tempRadius = self.neuron.nodes.loc[self.neuron.nodes['node_id'] == n, 'radius'].values[0] * Consts.SCF.value
            for ngh in self.neighbors[n]:
                edgeLengths.append(self.neuron.geodesic_matrix.at[n, ngh] * Consts.SCF.value)
                tempNeighborRadius = self.neuron.nodes.loc[self.neuron.nodes['node_id'] == ngh, 'radius'].values[0] * Consts.SCF.value
                sumRecip = sumRecip + 1 / (edgeLengths[-1] * tempRadius * ((1 / (tempNeighborRadius * tempNeighborRadius)) + (1 / (tempRadius * tempRadius))))

            avgEdgeLengths = sum(edgeLengths) / len(edgeLengths)
            rhs.at[n,n] = 1.0
            lhs.at[n,n] = 1 + (((2.0/3.0)* self.time_step * sumRecip) / (1.0 * Consts.RES.value * Consts.CAP.value * avgEdgeLengths))

            for n2 in self.neighbors[n]:
                tempNeighborRadius = self.neuron.nodes.loc[self.neuron.nodes['node_id'] == n2, 'radius'].values[0] * Consts.SCF.value
                lhs.at[n,n2] = -1.0*(2.0/3.0) * self.time_step / (1.0 * Consts.RES.value * Consts.CAP.value * tempRadius * avgEdgeLengths * n2 * ((1 / (tempNeighborRadius * tempNeighborRadius)) + (1 / (tempRadius * tempRadius))))

        return lhs, rhs
        
        

    # TODO:
    def solveStep(self, curStep):
        temp_state = np.full(self.neuron.nodes['node_id'].size, 0.0).astype("float64")
        self.u[-1] = (4.0 / 3.0) * self.r
        self.r = self.r + (((4.0/3.0) * self.time_step) * self.reactF(self.u[-1], self.n, self.m, self.h))
        self.r = self.r + ((-1.0/3.0) * self.u[-2])
        self.r = self.r + (((-2.0/3.0) * self.time_step) * self.reactF(self.u[-2], self.n_pre, self.m_pre, self.h_pre))
        self.r = self.r + self.isyn
        self.isyn = self.isyn * 0.0

        b = lu_solve((self.lu, self.piv), self.r)

        temp_state = self.n
        self.n = self.stateExplicitSBDF2(self.n, self.n_pre, self.fS(self.n, self.an(self.u[-1]), self.bn(self.u[-1])), self.fS(self.n_pre, self.an(self.u[-2]), self.bn(self.u[-2])), self.time_step)
        self.n_pre = temp_state

        temp_state = self.m
        self.m = self.stateExplicitSBDF2(self.m, self.m_pre, self.fS(self.m, self.am(self.u[-1]), self.bm(self.u[-1])), self.fS(self.m_pre, self.am(self.u[-2]), self.bm(self.u[-2])), self.time_step)
        self.m_pre = temp_state

        temp_state = self.h
        self.h = self.stateExplicitSBDF2(self.h, self.h_pre, self.fS(self.h, self.ah(self.u[-1]), self.bh(self.u[-1])), self.fS(self.h_pre, self.ah(self.u[-2]), self.bh(self.u[-2])), self.time_step)
        self.h_pre = temp_state

        self.u.append(b)
        # print(self.u)
        return

    def stateExplicitSBDF2(self, s, sPre, f, fPre, dt):
        s = np.add(np.multiply(f, dt), s)
        s = np.multiply(4.0/3.0, s)
        s = np.add(np.multiply(-1.0 / 3.0, sPre), s)
        s = np.add(np.multiply((-2.0 * dt) / 3.0, fPre), s)
        return s

    def fS(self, S, a, b):
        return (np.multiply(a, 1 - S) - np.multiply(b, S))

    def an(self, V):
        Vin = np.array(V)
        Vin = np.multiply(1.0e3, Vin)
        return 1e3 * 0.032 * np.divide(15.0 - Vin, ((15.0 - Vin) / 5.0) - 1.0)

    def bn(self, V):
        Vin = np.array(V)
        Vin = np. multiply(1e3, Vin)
        return 1e3 * 0.5 * ((10.0 - Vin) / 40.0)

    def am(self, V):
        Vin = np.array(V)
        Vin = np.multiply(1.0e3, Vin)
        return 1e3 * 0.32 * np.divide(13.0 - Vin, ((13.0 - Vin) / 4.0) - 1.0)

    def bm(self, V):
        Vin = np.array(V)
        Vin = np. multiply(1e3, Vin)
        return 1e3 * 0.28 * np.divide(Vin - 40.0, ((Vin - 40.0) / 5.0) - 1.0)

    def ah(self, V):
        Vin = np.array(V)
        Vin = np.multiply(1.0e3, Vin)
        return 1e3 * 0.128 * ((17.0 - Vin) / 18.0)

    def bh(self, V):
        Vin = np.array(V)
        Vin = np. multiply(1e3, Vin)
        return 1e3 * 4.0 / (((40.0 - Vin) / 5.0) + 1.0)

    def postSolve(self):
        return
        
        



    
    def print(self):
        print(self.neuron.nodes['node_id'].size)
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
        print(self.neuron)
        print(self.lu)
        # print(self.neuron.geodesic_matrix)
        # for i in range(len(self.neuron.edges)):
        #     print(self.neuron.geodesic_matrix.at[self.neuron.edges[i][0], self.neuron.edges[i][1]])
        #     print(self.distances[i])








if __name__ == "__main__":

    n = nv.read_swc("data/Green_19weeks_Neuron4.CNG.swc")


    

    #
    # Start of solving loop logic
    #
    t_pde = 0.008 * 1e-3
    t_sim = 0.01
    t_vis = 0.02
    endTime = 0.001
    totalSteps = (int)(endTime // t_pde)

    # main solving loop

    s = Solver("data/Green_19weeks_Neuron4.CNG.swc")
    # s.print()


    for curStep in range(totalSteps):
        s.solveStep(curStep)

    s.postSolve()
    # print(s.u)

    i = 0
    cmin = -0.000000001
    cmax = 0.0
    for i in range(len(s.u)):
        u = s.u[i].astype("float64")
        cmin = min(cmin,np.min(u))
        cmax = max(cmax,np.max(u))
        print(u)
        print(cmin)
        print(cmax)
        fig, ax = nv.plot2d(s.neuron, method='2d', view=('x', 'y'), color_by=u, vmin=cmin, vmax=cmax, palette="coolwarm" )

        # Save each incremental rotation as frame
        plt.savefig('outputs/frame{0}.png'.format(i))
        plt.close()
       # plt.show()



    print(totalSteps)

