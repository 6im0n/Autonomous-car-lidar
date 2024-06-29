#!/bin/bash

# Create two named pipes
mkfifo pipe1tmp
mkfifo pipe2tmp

# Start the Python program with its stdout redirected to pipe1 and its stdin redirected from pipe2
python3 LidarReader.py >pipe1 <pipe2 &

# Start the C program with its stdout redirected to pipe2 and its stdin redirected from pipe1
../../tek1/Need4Stek/ai >pipe2 <pipe1 &

# Wait for both programs to finish
wait

# Clean up the named pipes
rm pipe1 pipe2