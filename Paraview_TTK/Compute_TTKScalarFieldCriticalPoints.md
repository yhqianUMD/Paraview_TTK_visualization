## Below are the codes for computing discrete gradient on a tetrahedral mesh using the TTKScalarFieldCriticalPoints operator. The outputs in the console will be saved into a txt file. The input is a tetrahedral file in VTU format.

```
import time
import os

import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# --- Function to get peak memory usage from /proc/self/status (in MB)
def get_peak_memory_mb():
    try:
        with open('/proc/self/status', 'r') as f:
            for line in f:
                if 'VmHWM:' in line:  # High Water Mark = peak RSS
                    peak_kb = int(line.split()[1])
                    return peak_kb / 1024  # Convert to MB
    except Exception as e:
        print(f"Memory check failed: {e}")
    return None


# --- Start timing
start_time = time.time()

# ----------------------------------------------------------------
# Setup the data processing pipelines
# ----------------------------------------------------------------

# --- Load VTU file
brain_data_formatvtu = XMLUnstructuredGridReader(
    registrationName='GenericVTU.vtu',
    FileName=['/local/data/yuehui/pyspark/Tetra_mesh/data/NASA_tetra/Lander_small_data_format_streaming.vtu']
)
# brain_data_formatvtu.PointArrayStatus = ['Scalars_']
brain_data_formatvtu.TimeArray = 'None'

# --- Update pipeline (important to initialize data and metadata)
UpdatePipeline(proxy=brain_data_formatvtu)

# --- Detect scalar field dynamically if needed
available_arrays = list(brain_data_formatvtu.PointData.keys())

print("available_arrays:", available_arrays)

if not available_arrays:
    print(f"[Rank {rank}] ⚠️ No PointData arrays found. Skipping dataset.")
    exit(1)

preferred_names = ['Scalars_', 'Scalars']
scalar_name = next((name for name in preferred_names if name in available_arrays), available_arrays[0])
brain_data_formatvtu.PointArrayStatus = [scalar_name]

# --- Apply TTK ScalarFieldCriticalPoints filter
tTKScalarFieldCriticalPoints1 = TTKScalarFieldCriticalPoints(
    registrationName='TTKScalarFieldCriticalPoints1',
    Input=brain_data_formatvtu
)
tTKScalarFieldCriticalPoints1.ScalarField = ['POINTS', scalar_name]
tTKScalarFieldCriticalPoints1.InputOffsetField = ['POINTS', scalar_name]

# --- Update the pipeline to execute the filter
UpdatePipeline(proxy=tTKScalarFieldCriticalPoints1)

# --- End timing
end_time = time.time()
elapsed_time = end_time - start_time
peak_mem_mb = get_peak_memory_mb()
rank = os.environ.get("PMI_RANK") or os.environ.get("OMPI_COMM_WORLD_RANK") or "?"

# --- Output performance stats
print(f"📦 Using scalar array: {scalar_name}")
print(f"🧠 [Rank {rank}] Peak memory usage: {peak_mem_mb:.2f} MB")
print(f"⏱️  [Rank {rank}] Total processing time: {elapsed_time:.4f} seconds")

# ----------------------------------------------------------------
# Save critical points output (optional)
# ----------------------------------------------------------------
if __name__ == '__main__':
    pass
    # SaveData("critical_points_output.vtu", proxy=tTKScalarFieldCriticalPoints1)
    # SaveExtracts(ExtractsOutputDirectory='extracts')  # Optional
```
