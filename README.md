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


update visualization videos to make data 1fps and slow down number of extraps to make it actually visible

make it so that it only reads every other(for example) row of actual data instead of every row

make it more extreme

change actual update from 5 fps to 1 or 2fps 

make the update use the linear jump and linear nonjump methods of extrapolation

## Example combination ffmpeg command
```
ffmpeg -i EveryOtherSkipJumpComparison/center_1x0s2_2024_08_21-06_12_53_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x60s2j_2024_08_21-06_18_48_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x30s2_2024_08_21-06_15_26_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x60s2_2024_08_21-06_18_17_AM.mp4 -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]" -map "[v]" output.mp4

```

## Checklist
[] 1fps every datapoint jumps no extrap
[] 1fps every datapoint jumps 15fps extrap
[] 1fps every datapoint jumps 30fps extrap
[] 1fps every datapoint jumps 60fps extrap
[] 1fps every other datapoint jumps no extrap
[] 1fps every other datapoint jumps 15fps extrap
[] 1fps every other datapoint jumps 30fps extrap
[] 1fps every other datapoint jumps 60fps extrap

[] 1fps every datapoint no jumps no extrap
[] 1fps every datapoint no jumps 15fps extrap
[] 1fps every datapoint no jumps 30fps extrap
[] 1fps every datapoint no jumps 60fps extrap
[] 1fps every other datapoint no jumps no extrap
[] 1fps every other datapoint no jumps 15fps extrap
[] 1fps every other datapoint no jumps 30fps extrap
[] 1fps every other datapoint no jumps 60fps extrap
