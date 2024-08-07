# Steps
## Step One
Add this code to the SolveStep method in SparseSolverTestv1.cs (in Unity Project) at the end of the method, after defining `Upre` but before redefining `U_active`
```
using (StreamWriter sw = File.AppendText("/home/occam/Documents/code/neuropy/data/output.txt"))
{
sw.WriteLine(String.Join(",",Upre));
}
```
If you need the corresponding swc file, use the method the Neuron class creates to generate one.

## Step Two
Run the fromUnity.py to create the frames needed to create the non extrapolated version. 
Select the fps to correspond to desired lag.
Once the images are generated, convert to video
```
ffmpeg -framerate 30 -i 'outputs/frame%d.png' outputs/out.mp4
```

## Step Three
Edit fromUnity.py to generate extrapolated frames, and use 
```
ffmpeg -framerate 30 -i 'outputs/frame%d.png' outputs/out.mp4
```
changing the framerate to account for the additional frames
