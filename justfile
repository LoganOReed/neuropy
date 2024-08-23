# Makefile for neuropy

# Install project dependencies
install:
    poetry install

clean:
    rm -r outputs/*

# The first case (-e 0) only has -s as jump doesn't make sense
# without any extrapolation

# Build all examples with "center" data
center:
    poetry run extrap -d center -s 1 -f 1 -e 0 
    poetry run extrap -d center -s 2 -f 1 -e 0 
    poetry run extrap -d center -s 5 -f 1 -e 0 
    poetry run extrap -d center -s 1 -f 1 -e 15 
    poetry run extrap -d center -s 1 -f 1 -e 15 -j
    poetry run extrap -d center -s 2 -f 1 -e 15
    poetry run extrap -d center -s 2 -f 1 -e 15 -j
    poetry run extrap -d center -s 5 -f 1 -e 15
    poetry run extrap -d center -s 5 -f 1 -e 15 -j
    poetry run extrap -d center -s 1 -f 1 -e 30 
    poetry run extrap -d center -s 1 -f 1 -e 30 -j
    poetry run extrap -d center -s 2 -f 1 -e 30
    poetry run extrap -d center -s 2 -f 1 -e 30 -j
    poetry run extrap -d center -s 5 -f 1 -e 30
    poetry run extrap -d center -s 5 -f 1 -e 30 -j
    poetry run extrap -d center -s 1 -f 1 -e 60 
    poetry run extrap -d center -s 1 -f 1 -e 60 -j
    poetry run extrap -d center -s 2 -f 1 -e 60
    poetry run extrap -d center -s 2 -f 1 -e 60 -j
    poetry run extrap -d center -s 5 -f 1 -e 60
    poetry run extrap -d center -s 5 -f 1 -e 60 -j


# Build all examples with "endpoint" data
endpoint:
    poetry run extrap -d endpoint -s 1 -f 1 -e 0 
    poetry run extrap -d endpoint -s 2 -f 1 -e 0 
    poetry run extrap -d endpoint -s 5 -f 1 -e 0 
    poetry run extrap -d endpoint -s 1 -f 1 -e 15 
    poetry run extrap -d endpoint -s 1 -f 1 -e 15 -j
    poetry run extrap -d endpoint -s 2 -f 1 -e 15
    poetry run extrap -d endpoint -s 2 -f 1 -e 15 -j
    poetry run extrap -d endpoint -s 5 -f 1 -e 15
    poetry run extrap -d endpoint -s 5 -f 1 -e 15 -j
    poetry run extrap -d endpoint -s 1 -f 1 -e 30 
    poetry run extrap -d endpoint -s 1 -f 1 -e 30 -j
    poetry run extrap -d endpoint -s 2 -f 1 -e 30
    poetry run extrap -d endpoint -s 2 -f 1 -e 30 -j
    poetry run extrap -d endpoint -s 5 -f 1 -e 30
    poetry run extrap -d endpoint -s 5 -f 1 -e 30 -j
    poetry run extrap -d endpoint -s 1 -f 1 -e 60 
    poetry run extrap -d endpoint -s 1 -f 1 -e 60 -j
    poetry run extrap -d endpoint -s 2 -f 1 -e 60
    poetry run extrap -d endpoint -s 2 -f 1 -e 60 -j
    poetry run extrap -d endpoint -s 5 -f 1 -e 60
    poetry run extrap -d endpoint -s 5 -f 1 -e 60 -j

jump-comparison:
    poetry run extrap -d endpointFull -s 10 -e 30
    poetry run extrap -d endpointFull -s 10 -e 30 -j
    ffmpeg -i endpointFull_10s30e.mp4 -i endpointFull_10s30ej.mp4 -filter_complex hstack jumpComparison_10s30e.mp4
    poetry run extrap -d endpointFull -s 15 -e 30
    poetry run extrap -d endpointFull -s 15 -e 30 -j
    ffmpeg -i endpointFull_15s30e.mp4 -i endpointFull_15s30ej.mp4 -filter_complex hstack jumpComparison_15s30e.mp4

intro-example:
    poetry run extrap -d center -s 5
    poetry run extrap -d center -s 5 -e 15 -j
    poetry run extrap -d center -s 5 -e 30
    poetry run extrap -d center -s 5 -e 30 -j
    ffmpeg -i center_5s0e.mp4 -i center_5s15ej.mp4 -i center_5s30e.mp4 -i center_5s30ej.mp4 -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]" -map "[v]" output.mp4



# Build entire example suite
examples: center endpoint

default: install
    
