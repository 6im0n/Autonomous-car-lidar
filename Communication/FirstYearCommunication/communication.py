"""import subprocess
import os

# Start the C program
c_process = subprocess.Popen(
    ['../tek1/Need4Stek/ai'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Start the Python program
python_process = subprocess.Popen(
    ['python3', 'LidarRetroEngineering/LidarReader.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Function to handle communication between the processes
def communicate():
    while True:
        # Read from the C program's stdout and write to the Python program's stdin
        c_output = c_process.stdout.readline()
        print("C output: ", c_output)
        if c_output:
            python_process.stdin.write(c_output)
            python_process.stdin.flush()

        # Read from the Python program's stdout and write to the C program's stdin
        python_output = python_process.stdout.readline()
        print("Python output: ", python_output)
        if python_output:
            c_process.stdin.write(python_output)
            c_process.stdin.flush()

try:
    communicate()
except KeyboardInterrupt:
    c_process.terminate()
    python_process.terminate()"""


import subprocess
import threading
import sys

# Function to handle communication between the processes
def communicate(c_process, python_process):
    try:
        while True:
            # Read from the C program's stdout and write to the Python program's stdin
            c_output = c_process.stdout.readline()
            if c_output:
                print("C output:", c_output.strip())
                python_process.stdin.write(c_output)
                python_process.stdin.flush()

            # Read from the Python program's stdout and write to the C program's stdin
            python_output = python_process.stdout.readline()
            if python_output:
                print("Python output:", python_output.strip())
                c_process.stdin.write(python_output)
                c_process.stdin.flush()

    except KeyboardInterrupt:
        print("Interrupted by user. Terminating processes.")
    except BrokenPipeError as e:
        print(f"BrokenPipeError: {e}", file=sys.stderr)
    finally:
        c_process.terminate()
        python_process.terminate()
        print("Processes terminated.")

# Start the C program
c_process = subprocess.Popen(
    ['../tek1/Need4Stek/ai'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Start the Python program
python_process = subprocess.Popen(
    ['python3', 'LidarRetroEngineering/LidarReader.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    communicate(c_process, python_process)
except KeyboardInterrupt:
    c_process.terminate()
    python_process.terminate()