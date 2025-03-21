# Paraview and TTK installation on a cluster, with MPI supported

## Introduction
This tutorial is an introduction for configuring Paraview and TTK on a cluster without sudo access and GUI. The main steps are referred to https://github.com/eve-le-guillou/TTK-MPI-at-example.

## Install Paraview
1) git clone using putty
   
   go to the directory where we want to install Paraview, then clone ttk-paraview using putty. Sometimes it showed an error when using VScode terminal for clone.
   git clone https://github.com/topology-tool-kit/ttk-paraview.git
   
2) check out the specific version
   
   cd ttk-paraview
   git checkout 5.11.0
   
3) build
   
  mkdir build && cd build
  
4) cmake or ccmake

   if using cmake:
    cmake -DCMAKE_BUILD_TYPE=Release -DPARAVIEW_USE_PYTHON=ON -DPARAVIEW_USE_MPI=ON -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON -DCMAKE_INSTALL_PREFIX=../install ..
   if using ccmake, we can change the configuration one by one (we use the cmake of version 3.23 as the newest version do not have ccmake):
   ../../cmake-3.23.0/bin/ccmake ../

   Note: remember to disable qt as we do not have GUI on this cluster
   
5) make install, replace the 4 in make -j4 install by the number of cores available

   make -j4 install

## TTK installation

```
cd ~
git clone https://github.com/topology-tool-kit/ttk.git
cd ttk
git checkout c701cd60b5432d5efe1e63442c3db2998ff383d8
mkdir build && cd build
PARAVIEW_PATH=~/ttk-paraview/install/lib/cmake/paraview-5.11
cmake -DParaView_DIR=$PARAVIEW_PATH -DTTK_ENABLE_MPI=ON -DTTK_ENABLE_MPI_TIME=ON 
-DTTK_ENABLE_64BITS_IDS=ON -DCMAKE_INSTALL_PREFIX=../install .. 
make -j4 install
```

Notes:
* Similarly to the installation of Paraview, we will use ccmake instead of cmake. In addition, we need to remove the "master" before "num_threads" when encountering this kind of error.
* Change the directory of VTK_DIR from the environment in conda (which I installed previously) to the one in current paraview, like "/local/data/yuehui/local_yh/ttk-paraview/install/lib64/cmake/paraview-5.11/vtk".
* Again, replace the 4 in make -j4 install by the number of cores available.

## Update environment variables
```
export PATH=$PATH:/local/data/yuehui/local_yh/ttk-paraview/install/bin/
TTK_PREFIX=/local/data/yuehui/local_yh/ttk/install
export PV_PLUGIN_PATH=$TTK_PREFIX/bin/plugins/TopologyToolKit
export LD_LIBRARY_PATH=$TTK_PREFIX/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=$TTK_PREFIX/lib64/python3.9/site-packages
```

Notes:
* Remember to change "lib" to "lib64", e.g., from "export PYTHONPATH=$TTK_PREFIX/lib/python3.9/site-packages" to "export PYTHONPATH=$TTK_PREFIX/lib64/python3.9/site-packages"

## Run the example
1) retrieve the TTK-MPI-at_example
   
   https://github.com/eve-le-guillou/TTK-MPI-at-example.git
2) By default, the example is resampled to 256^3. To execute it using 2 threads and 4 processes, use the following command:
   
   OMP_NUM_THREADS=2 mpirun -n 4 pvbatch pipeline.py
