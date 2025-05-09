# Paraview and TTK installation on a cluster, with MPI support

## Introduction
This tutorial is an introduction for configuring Paraview and TTK on a cluster without sudo access and GUI. The main steps are referred to https://github.com/eve-le-guillou/TTK-MPI-at-example.

* Remember to create and activate a Python virtual environment using conda, as we will use Python to run the MPT-supported TTK after the installation.

   ```
   conda activate py39
   ```
* Load necessary modules
  ```
  module load rh9/mpich/4.3.0
  module load boost/1.84.0
  module load git/2.29.3
  module load python/3.8/anaconda
  ```

## Install Paraview
1) git clone using Putty
   
   go to the directory where we want to install Paraview, then clone ttk-paraview using Putty. Sometimes it showed an error when using VScode terminal for clone.
   ```
   git clone https://github.com/topology-tool-kit/ttk-paraview.git
   ```
   
3) check out the specific version
   
   ```
   cd ttk-paraview
   ```
   
4) build
   
   ```
   mkdir build && cd build
   ```
  
4) cmake or ccmake

   * if using cmake:
       ```
       cmake -DCMAKE_BUILD_TYPE=Release -DPARAVIEW_USE_PYTHON=ON -DPARAVIEW_USE_MPI=ON -DPARAVIEW_USE_QT=OFF -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON -DCMAKE_INSTALL_PREFIX=../install ..
       ```
   * if using ccmake, we can change the configuration one by one (we use the cmake of version 3.23 as the newest version do not have ccmake):
      ```
      /gpfs/data1/cgis1gp/yuehui/cmake-3.26.0/bin/ccmake ../
      ```

   Note: remember to disable qt as we do not have GUI on this cluster; also remember to set other attributes like using cmake
   
5) make install, replace the 4 in make -j4 install with the number of cores available

   ```
   make -j4 install
   ```
   or, we can directly use ```make -j install```

## TTK installation

* git clone ttk
   ```
   cd /gpfs/data1/cgis1gp/yuehui/local_yh
   git clone https://github.com/topology-tool-kit/ttk.git
   cd ttk
   mkdir build && cd build
   ```
* configure
   ```
   PARAVIEW_PATH=~/ttk-paraview/install/lib64/cmake/paraview-5.13
   cmake -DParaView_DIR=$PARAVIEW_PATH -DTTK_ENABLE_MPI=ON -DTTK_ENABLE_MPI_TIME=ON 
   -DTTK_ENABLE_64BITS_IDS=ON -DCMAKE_INSTALL_PREFIX=../install -DVTK_DIR=/gpfs/data1/cgis1gp/yuehui/local_yh/ttk-paraview/install/lib64/cmake/paraview-5.13/vtk -DBoost_INCLUDE_DIR=/apps/boost/1.84.0/include ..
   ```
* install
  ```
  make -j install
  ```
  or
  ```
   make -j4 install
   ```

Notes:
* Similarly to the installation of Paraview, we will use ccmake instead of cmake. In addition, we need to remove the "master" before "num_threads" when encountering this kind of error.
* Change the directory of VTK_DIR from the environment in conda (which I installed previously) to the one in current paraview, like "/gpfs/data1/cgis1gp/yuehui/local_yh/ttk-paraview/install/lib64/cmake/paraview-5.13/vtk".
* Again, replace the 4 in make -j4 install by the number of cores available.

## Update environment variables temporarily
```
export PATH=$PATH:/gpfs/data1/cgis1gp/yuehui/local_yh/ttk-paraview/install/bin/
TTK_PREFIX=/gpfs/data1/cgis1gp/yuehui/local_yh/ttk/install
export PV_PLUGIN_PATH=$TTK_PREFIX/bin/plugins/TopologyToolKit
export LD_LIBRARY_PATH=$TTK_PREFIX/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=$TTK_PREFIX/lib64/python3.9/site-packages
```

## Update environment variables permanently
```
echo 'export PATH=$PATH:/gpfs/data1/cgis1gp/yuehui/local_yh/ttk-paraview/install/bin/' >> ~/.bashrc
echo 'export TTK_PREFIX=/gpfs/data1/cgis1gp/yuehui/local_yh/ttk/install' >> ~/.bashrc
echo 'export PV_PLUGIN_PATH=$TTK_PREFIX/bin/plugins/TopologyToolKit' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$TTK_PREFIX/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PYTHONPATH=$TTK_PREFIX/lib64/python3.9/site-packages' >> ~/.bashrc
source ~/.bashrc
```

Notes:
* Remember to change "lib" to "lib64", e.g., from "export PYTHONPATH=$TTK_PREFIX/lib/python3.9/site-packages" to "export PYTHONPATH=$TTK_PREFIX/lib64/python3.9/site-packages"

## Run the example
### test with TTK-MPI examples
1) retrieve the TTK-MPI-at_example
   
   https://github.com/eve-le-guillou/TTK-MPI-at-example.git
2) By default, the example is resampled to 256^3. To execute it using 2 threads and 4 processes, use the following command:
   
   ```
   module load rh9/mpich/4.3.0
   OMP_NUM_THREADS=2 mpirun -n 4 pvbatch pipeline.py
   ```

### test with TTK discrete gradient examples
1) create a gsappx.machinefile file with the following contents in this file:
   ```
   gsappx1.gshpc.umd.edu:8
   gsappx2.gshpc.umd.edu:8
   gsappx3.gshpc.umd.edu:8
   gsappx4.gshpc.umd.edu:8
   ```
   Note: '8' refers to the number of ranks or processes that we would like to request on each node. In this cluster, gsappx1-4 each has 16 cores. If we request it as '8', it means that we will have 2 threads for each rank or process and we have 32 processes in total.
   
2) export the number of threads
   ```
   export OMP_NUM_THREADS=2
   ```

3) go to the directory that contains the gsappx.machinefile
   ```
   cd /gpfs/data1/cgis1gp/yuehui/codes/MPI_Python
   ```

4) load MPICH
   ```
   module load rh9/mpich/4.3.0
   ```
   
5) run the MPI programs
   ```
   mpiexec -machinefile gsappx.machinefile -n 32 pvbatch /gpfs/data1/cgis1gp/yuehui/codes/MPI_Python/gradient_general_purpose_separate_timing_triangle_mesh_noOutputs_04162025.py
   ```

