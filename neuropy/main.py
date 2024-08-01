import numpy 
import navis
import pandas

if __name__ == "__main__":
    n = navis.example_neurons(n=1,kind='skeleton')
    n = navis.read_swc("data/Green_19weeks_Neuron4.CNG.swc")
    print(n)
    
