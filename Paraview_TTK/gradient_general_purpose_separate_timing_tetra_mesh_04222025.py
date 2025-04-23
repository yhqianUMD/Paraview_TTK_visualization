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
