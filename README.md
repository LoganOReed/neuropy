To convert png outputs to a video
```
ffmpeg -framerate 30 -pattern_type glob -i 'outputs/*.png'    outputs/out.mp4
```
