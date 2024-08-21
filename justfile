# Makefile for neuropy

# Install project dependencies
install:
    poetry install

clean:
    rm -r outputs/*

# The first case (-e 0) only has -s as jump doesn't make sense
# without any extrapolation
center:
    poetry run extrap -d center -f 1 -e 0 
    poetry run extrap -d center -f 1 -e 0 -s
    poetry run extrap -d center -f 1 -e 15 
    poetry run extrap -d center -f 1 -e 15 -j
    poetry run extrap -d center -f 1 -e 15 -s
    poetry run extrap -d center -f 1 -e 15 -js
    poetry run extrap -d center -f 1 -e 30 
    poetry run extrap -d center -f 1 -e 30 -j
    poetry run extrap -d center -f 1 -e 30 -s
    poetry run extrap -d center -f 1 -e 30 -js
    poetry run extrap -d center -f 1 -e 60 
    poetry run extrap -d center -f 1 -e 60 -j
    poetry run extrap -d center -f 1 -e 60 -s
    poetry run extrap -d center -f 1 -e 60 -js



endpoint:
    poetry run extrap -d endpoint -f 1 -e 0 
    poetry run extrap -d endpoint -f 1 -e 0 -s
    poetry run extrap -d endpoint -f 1 -e 15 
    poetry run extrap -d endpoint -f 1 -e 15 -j
    poetry run extrap -d endpoint -f 1 -e 15 -s
    poetry run extrap -d endpoint -f 1 -e 15 -js
    poetry run extrap -d endpoint -f 1 -e 30 
    poetry run extrap -d endpoint -f 1 -e 30 -j
    poetry run extrap -d endpoint -f 1 -e 30 -s
    poetry run extrap -d endpoint -f 1 -e 30 -js
    poetry run extrap -d endpoint -f 1 -e 60 
    poetry run extrap -d endpoint -f 1 -e 60 -j
    poetry run extrap -d endpoint -f 1 -e 60 -s
    poetry run extrap -d endpoint -f 1 -e 60 -js

# Run the development environment (install, run, and watch for changes)
run: center endpoint

default: install
    
