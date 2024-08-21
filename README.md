# How to Use
This repo holds the code used to generate the visualizations and most permutations of the options.
The only info needed to view the results is how to understand the output video's names.

## How to Read the Output Names
Here is an example filename
```
center_2s30ej.mp4
```
It starts with the name of the data file, e.g. "center", which is always followed by an underscore.
Then there will a number followed by s, which shows how often the data rows are skipped (hence the s).
For example, "2s" means it uses every other, "5s" means it uses every fifth.
Then there will be a number followed by e, which is the number of distinct points shown during the linear extrapolation process.
Lastly, the optional "j" indicates that the visualization jumps to the calculated value instead of using an approximate point found during extrapolation to smooth the visualization.

## How to Run the Code
Because the code runs on poetry, as long as you have python3.9 and poetry you should be able to run 
```
poetry install
```
and have all of the dependencies work themselves out. The main way of calling the code is to use the "extrap" script defined through poetry, for example
```
poetry run extrap -d center -s 4 -p -e 5
```
All of the code is found in "neuropy/extrapolateFromData.py"

### Warning
Due to the code using "ffmpeg" to convert .pngs into .mp4's the host machine needs to have that installed.
The code also uses "subprocesses" which behave slightly differently depending on the OS, but mac and linux machines should have no problems (windows is wholly untested).


## Generating New Morphologies and Data Files
Add this code to the SolveStep method in SparseSolverTestv1.cs (in Unity Project) at the end of the method, after defining `Upre` but before redefining `U_active`
```
using (StreamWriter sw = File.AppendText("/home/occam/Documents/code/neuropy/data/output.txt"))
{
sw.WriteLine(String.Join(",",Upre));
}
```
If you need the corresponding swc file, use the method the Neuron class creates to generate one.

## Example combination ffmpeg command
If additional styling is desired, here is an example of creating a 2x2 grid with various configurations
```
ffmpeg -i EveryOtherSkipJumpComparison/center_1x0s2_2024_08_21-06_12_53_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x60s2j_2024_08_21-06_18_48_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x30s2_2024_08_21-06_15_26_AM.mp4 -i EveryOtherSkipJumpComparison/center_1x60s2_2024_08_21-06_18_17_AM.mp4 -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]" -map "[v]" output.mp4
```

