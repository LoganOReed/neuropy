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
    poetry run extrap -d center -s 1 -f 1 -e 5 
    poetry run extrap -d center -s 1 -f 1 -e 5 -j
    poetry run extrap -d center -s 2 -f 1 -e 5
    poetry run extrap -d center -s 2 -f 1 -e 5 -j
    poetry run extrap -d center -s 5 -f 1 -e 5
    poetry run extrap -d center -s 5 -f 1 -e 5 -j
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

center-extra:
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
    poetry run extrap -d endpoint -s 1 -f 1 -e 5 
    poetry run extrap -d endpoint -s 1 -f 1 -e 5 -j
    poetry run extrap -d endpoint -s 2 -f 1 -e 5
    poetry run extrap -d endpoint -s 2 -f 1 -e 5 -j
    poetry run extrap -d endpoint -s 5 -f 1 -e 5
    poetry run extrap -d endpoint -s 5 -f 1 -e 5 -j
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

endpoint-extra:
    poetry run extrap -d endpoint -s 1 -f 1 -e 60 
    poetry run extrap -d endpoint -s 1 -f 1 -e 60 -j
    poetry run extrap -d endpoint -s 2 -f 1 -e 60
    poetry run extrap -d endpoint -s 2 -f 1 -e 60 -j
    poetry run extrap -d endpoint -s 5 -f 1 -e 60
    poetry run extrap -d endpoint -s 5 -f 1 -e 60 -j

jump-comparison:
    poetry run extrap -d endpointFull -s 10 -e 30
    poetry run extrap -d endpointFull -s 10 -e 30 -j
    ffmpeg -y -i outputs/endpointFull_10s30e.mp4 -i outputs/endpointFull_10s30ej.mp4 -filter_complex hstack outputs/jumpComparison_10s30e.mp4
    poetry run extrap -d endpointFull -s 15 -e 30
    poetry run extrap -d endpointFull -s 15 -e 30 -j
    ffmpeg -y -i outputs/endpointFull_15s30e.mp4 -i outputs/endpointFull_15s30ej.mp4 -filter_complex hstack outputs/jumpComparison_15s30e.mp4

basic-comparison:
    poetry run extrap -d center -s 5
    poetry run extrap -d center -s 5 -e 15 -j
    poetry run extrap -d center -s 5 -e 30
    poetry run extrap -d center -s 5 -e 30 -j
    ffmpeg -y -i outputs/center_5s0e.mp4 -i outputs/center_5s15ej.mp4 -i outputs/center_5s30e.mp4 -i outputs/center_5s30ej.mp4 -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]" -map "[v]" outputs/basicComparison.mp4



# Build most of the example suite
examples: center endpoint jump-comparison basic-comparison

# Builds all examples, including the most expensive ones
examples-full: examples center-extra endpoint-extra

default: install
    
