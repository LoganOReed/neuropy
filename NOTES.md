# Notes for Meeting

# General TODO
1. Add an additional values field which stores previous values (for visualization)


NOTE: - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/NeuronalDynamics/Simulation/ExampleNDSolver.cs doesn't actually do anything for us, SparseSolver is the actual one.


## TODO Today
1. Change t_sim and t_vis to mimic slowdowns
1a. Potentially try fluxuating t_sim
2. Add t_comp and try values greater than t_sim
3. Can I find values which cause notable problems
4. Implement a simple function in place of Richardson Extrap to test basic structure
5. Write overview of R.E so I can speak knowledgably about it
6. Add debug output

## Questions
1. How do we map the 1d results to the mesh?
2. How are the meshes defined and why is it so horrible.
3. What are the next steps regarding studying stability and convergence.

## Concerns
1. There is massive technical debt with the codebase, the vast majority of the work I've done is figuring out what the code does and where
2. Testing cases is very difficult as you have to connect everything by hand every time
3. Because of how the meshes are defined it is nontrivial to add new morphologies, and the current code uses a unique datastructure instead of the standard format 
3a. This is .swc which is [here](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html)

## Locations
t_sim - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/Simulation.cs#54
      - 0.01f
t_vis - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/Simulation.cs#59
      - 0.02f
t_pde - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/Simulation.cs#59
      - 0.008 * 1e-3

PostSolveStep - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/NeuronalDynamics/Simulation/NDSimulation.cs#205


UpdateVisualization - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/MeshSimulation.cs#91
1. Converts sim vals to color vals
UpdateVisualizationStep - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/Simulation.cs#142
1. Get's simulation values
2. Calls UpdateVisualization (which converts sim vals to color vals)
3. Waits until the next Visualization Time Step

GetValues - /documents/code/NeuroVISOR/Assets/Scripts/C2M2/NeuronalDynamics/Simulation/NDSimulation.cs#295
1. Translate 1D vertex to 3D Vertex and pass up for visualization
2. Seemingly only used here /documents/code/NeuroVISOR/Assets/Scripts/C2M2/Simulation/Simulation.cs#142 to call UpdateVisualization


### C Sharp Specific Notes
The functions using an "in" parameter are passing by readonly reference. See [this](https://stackoverflow.com/questions/52820372/why-would-one-ever-use-the-in-parameter-modifier-in-c)


# Aug 16 NOTES

TODO Make a writeup

update visualization videos to make data 1fps and slow down number of extraps to make it actually visible

make it so that it only reads every other(for example) row of actual data instead of every row

make it more extreme

change actual update from 5 fps to 1 or 2fps 

make the update use the linear jump and linear nonjump methods of extrapolation
