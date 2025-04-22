Below are the codes for computing discrete gradient on a triangle mesh using the TTKDiscreteGradient operator. The outputs in console will be saved into a txt file. The input is a TIN file in VTK format.
```
import sys
import time
import os
import subprocess
from paraview.simple import *

date = time.strftime("%m,%d,%Y")
date_name = date.split(',')[0] + date.split(',')[1] + date.split(',')[2]

# Path to your input file
input_file = "/local/data/yuehui/pyspark/data/Morse_Spark_datasets/NAPA_out_xyz.vtk"

print(f"Loading input file: {input_file}")

directory = os.path.dirname(input_file)
tin_basename = os.path.basename(input_file)
tin_filename = os.path.splitext(tin_basename)[0]
log_file = os.path.join(directory, tin_filename + "_" + date_name + ".txt")

def get_peak_memory_mb():
    try:
        with open('/proc/self/status', 'r') as f:
            for line in f:
                if 'VmHWM:' in line:
                    peak_kb = int(line.split()[1])
                    return peak_kb / 1024
    except Exception as e:
        print(f"Memory check failed: {e}")
    return None

rank = os.environ.get("PMI_RANK") or os.environ.get("OMPI_COMM_WORLD_RANK") or "?"

# ========== 🔁 Full stdout/stderr redirection using low-level OS file descriptors ==========
# Save original stdout/stderr fds
original_stdout_fd = os.dup(1)
original_stderr_fd = os.dup(2)

with open(log_file, "w") as log_f:
    os.dup2(log_f.fileno(), 1)  # Redirect stdout
    os.dup2(log_f.fileno(), 2)  # Redirect stderr

    try:
        # Start timing
        start_time = time.time()

        # Run pipeline
        mesh = OpenDataFile(input_file)
        mesh.UpdatePipeline()

        print("Input mesh loaded. Applying TTK Discrete Gradient...")

        discreteGradient = TTKDiscreteGradient(Input=mesh)
        discreteGradient.UpdatePipeline()

        # End timing
        end_time = time.time()
        total_time = end_time - start_time

        # Peak memory
        peak_mem_mb = get_peak_memory_mb()
        print(f"🧠 [Rank {rank}] Peak memory usage: {peak_mem_mb:.2f} MB")
        print(f"⏱️  [Rank {rank}] Total time cost: {total_time:.4f} seconds")

    finally:
        # Restore original stdout/stderr
        os.dup2(original_stdout_fd, 1)
        os.dup2(original_stderr_fd, 2)
```
