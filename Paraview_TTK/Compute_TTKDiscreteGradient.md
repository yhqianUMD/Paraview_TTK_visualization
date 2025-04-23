## 1. Below are the codes (gradient_general_purpose_separate_timing_triangle_mesh_04162025.py) for computing discrete gradient on a triangle mesh using the TTKDiscreteGradient operator. The outputs in the console will be saved into a txt file. The input is a TIN file in VTK format.
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

## 2. Below are the codes (gradient_general_purpose_separate_timing_tetra_mesh_04222025.py) for computing discrete gradient on a tetrahedral mesh using the TTKDiscreteGradient operator. The outputs in the console will be saved into a txt file. The input is a tetrahedral file in VTU format.

```
import time
import os
import sys
from paraview.simple import *

# Ensure ParaView compatibility
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11
paraview.simple._DisableFirstRenderCameraReset()

# ========== Configuration ==========
input_file = "/local/data/yuehui/pyspark/Tetra_mesh/data/tetrahedron_data_format.vtu"
directory = os.path.dirname(input_file)
basename = os.path.basename(input_file)
base_filename = os.path.splitext(basename)[0]
date_name = time.strftime("%m%d%Y")
log_file = os.path.join(directory, f"{base_filename}_{date_name}.txt")

# MPI rank
rank = os.environ.get("PMI_RANK") or os.environ.get("OMPI_COMM_WORLD_RANK") or "?"

# ========== Peak Memory Function ==========
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

# ========== Logging Setup ==========
original_stdout = sys.stdout
original_stderr = sys.stderr
original_stdout_fd = os.dup(1)
original_stderr_fd = os.dup(2)

with open(log_file, "w") as log_f:
    # Redirect stdout and stderr
    sys.stdout = log_f
    sys.stderr = log_f
    os.dup2(log_f.fileno(), 1)
    os.dup2(log_f.fileno(), 2)

    try:
        # --- LOGGING STARTS ---
        print(f"📋 Log File: {log_file}")
        print(f"🟢 [Rank {rank}] Starting TTK Discrete Gradient computation")
        print(f"📂 Input File: {input_file}")
        sys.stdout.flush()

        start_time = time.time()

        # --- Load Mesh
        if input_file.endswith('.vtu'):
            mesh_input = XMLUnstructuredGridReader(
                registrationName='InputMesh',
                FileName=[input_file]
            )
        elif input_file.endswith('.ts'):
            mesh_input = TTKTopologicalSimplificationReader(
                registrationName='InputMesh',
                FileName=[input_file]
            )
        else:
            raise ValueError("Unsupported file format. Use .vtu or .ts.")
        
        UpdatePipeline(proxy=mesh_input)
        print("✅ Mesh loaded successfully")
        sys.stdout.flush()

        # --- Apply Discrete Gradient
        start_grad_time = time.time()
        discrete_gradient = TTKDiscreteGradient(
            registrationName='DiscreteGradient',
            Input=mesh_input
        )
        discrete_gradient.GetClientSideObject()
        UpdatePipeline(proxy=discrete_gradient)
        grad_time = time.time() - start_grad_time

        print("✅ TTKDiscreteGradient computation completed")
        sys.stdout.flush()

        # --- Final Stats
        total_time = time.time() - start_time
        peak_mem = get_peak_memory_mb()

        print(f"🧠 [Rank {rank}] Peak Memory: {peak_mem:.2f} MB")
        print(f"⏱️  [Rank {rank}] Gradient Time: {grad_time:.4f} sec")
        print(f"⏱️  [Rank {rank}] Total Time: {total_time:.4f} sec")
        sys.stdout.flush()

    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        os.dup2(original_stdout_fd, 1)
        os.dup2(original_stderr_fd, 2)

if __name__ == '__main__':
    pass
```
