import numpy 
import navis
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # n = navis.example_neurons(n=1,kind='skeleton')
    n = navis.read_swc("data/Green_19weeks_Neuron4.CNG.swc")
    fig, ax = navis.plot2d(n, method='2d', view=('x', 'y'), depth_coloring=True)
    plt.show()
    print(n.nodes)
    
