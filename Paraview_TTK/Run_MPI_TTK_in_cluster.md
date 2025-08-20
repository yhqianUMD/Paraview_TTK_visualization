# Steps to run MPI-supported TTK on a cluster

* 1) ssh to gsappx1 cluster
  ```
  ssh qiany@gsappx1
  ```
  
* 2) load necessary modules
  ```
  module load openmpi/3.1.0
  module load gcc/12.3.0
  module load boost/1.84.0 (may not necessary)
  ```

Option 1:
* 3) go to the directory where the Python script is stored
  ```
  cd /gpfs/data1/cgis1gp/yuehui/codes/MPI_Python
  ```

* 4) set the number of threads to use
  ```
  OMP_NUM_THREADS=16
  ```

* 5) run the python script to compute discrete gradient
  ```
  mpiexec -machinefile gsappx.machinefile -n 4 pvbatch --mpi script.py
  ```

Notes:
* put gsappx.machinefile in the directory /gpfs/data1/cgis1gp/yuehui/codes/MPI_Python
* set gsappx.machinefile as the following if we would like to use 4 processes in total
  ```
  gsappx1.gshpc.umd.edu:1
  gsappx2.gshpc.umd.edu:1
  gsappx3.gshpc.umd.edu:1
  gsappx4.gshpc.umd.edu:1
  ```

Option 2:
* 3) go to the directory where ttk-paraview is installed
  ```
  cd /local/data/yuehui/local_yh/ttk-paraview/build/bin
  ```
* 4) compute discrete gradient
  ```
  OMP_NUM_THREADS=6 mpirun -n 20 pvbatch pipeline.py
  ```
