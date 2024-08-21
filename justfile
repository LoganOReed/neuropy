# Makefile for neuropy

# Install project dependencies
install:
    poetry install

clean:
    rm -r outputs/*

# The first case (-e 0) only has -s as jump doesn't make sense
# without any extrapolation

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





# Run the development environment (install, run, and watch for changes)
run: center endpoint

default: install
    
