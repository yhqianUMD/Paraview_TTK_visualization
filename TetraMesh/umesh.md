# The following are techniques for tetrahedralizing a mesh

## 1. git clone https://github.com/guoxiliu/umesh-wald.git, using the cmake for tetrahedralization, here are the detailed steps
   1) git clone https://github.com/guoxiliu/umesh-wald.git
   2) mkdir "build" in the "umesh-wald" folder
   3) cd build, then "module load cmake/3.10.0" and "module load gcc/8.3.1"
      module rm cmake/3.16.0 when needed
      Note:
      -a) if the cmake version is not compatible, we can download the cmake file from official website.
      
      -b) Go to https://github.com/Kitware/CMake/releases/tag/v3.26.0 and download the out-of-box version cmake-3.26.0-linux-x86_64.sh
      
      -c) Go to the folder of "cmake-3.26.0-linux-x86_64.sh" in the cluster, type command "chmod +x cmake-3.26.0-linux-x86_64.sh"
      
      -d) Then, type "./cmake-3.26.0-linux-x86_64.sh", type "Y" until it has been successfully installed
      
      -e) Go to the bin folder, use the "./ccmake --version" to check its version
      
      -f) Rename foler cmake-3.26.0-linux-x86_64 as cmake-3.26.0
      
      -g) Remove previous cmake by "module rm cmake/3.16.0"
      
      -h) Use the new cmake. As the folder "cmake-3.26.0" is within the folder of "umesh-wald" and outside of "build" foler, type "../cmake-3.26.0/bin/ccmake ../"
      
      -i) Remember to modify back the CMakeList.txt, replace "cmake_minimum_required(VERSION 3.10)" with "cmake_minimum_required(VERSION 3.16)", 3.16 is the original one
      
  5) After "../cmake-3.26.0/bin/ccmake ../", type "c" then "g"
  6) Within the "build" folder, type "make"
  7) Tetrahedralize by "./umeshTetrahedralize -o output_1.umesh input.umesh"
  8) WriteTS by "./writeTS -o output.ts output_1.umesh"
     Notes:
     -a) Show the first 20 rows: head -n 20 output.ts
     
     -b) Show the last 20 rows: tail -n 20 output.ts

## 2. tetrahedralization through paraview
   1) install paraview in Linux cluster, go to https://www.paraview.org/download/ and download the out-of-box version "ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz"
   2) put the downloaded "ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz" within the folder "/gpfs/data1/cgis1gp/yuehui/Paraview"
   3) tar -xvzf ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz
   4) Rename the folder, "mv ParaView-5.10.1-MPI-Linux-Python3.9-x86_64 ParaView-5.10.1"
   5) Go to "bin" folder, directly use the "pvpython" for tetrahedralization
   6) type "./pvpython test.py input.raw output.vtu" for tetrahedralization
      Note: Remember to change the data properties of the input file (e.g., the data type, spacing, origin)
      -a) change rawData.DataScalarType
      
      -b) change rawData.DataOrigin
      
      -c) change rawData.DataSpacing
      
      -d) change rawData.DataExtent
      
      -e) set threshold,
      ```
         threshold1.LowerThreshold = 5
         threshold1.UpperThreshold = 5008
         threshold1.ThresholdMethod = vtkThreshold.THRESHOLD_BETWEEN
         # threshold1.ThresholdRange = [150, 270]
      ```
   
