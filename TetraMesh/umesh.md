The following are techniques for tetrahedralizing a mesh

1. git clone https://github.com/guoxiliu/umesh-wald.git, using the cmake for tetrahedralization, here are the detailed steps
   1) git clone https://github.com/guoxiliu/umesh-wald.git
   2) mkdir "build" in the "umesh-wald" folder
   3) cd build, then "module load cmake/3.10.0" and "module load gcc/8.3.1"
      - module rm cmake/3.16.0 when needed
      Note:
      a) if the cmake version is not compatible, we can download the cmake file from official website.
      b) Go to https://github.com/Kitware/CMake/releases/tag/v3.26.0 and download the out-of-box version cmake-3.26.0-linux-x86_64.sh
      c) Go to the folder of "cmake-3.26.0-linux-x86_64.sh" in the cluster, type command "chmod +x cmake-3.26.0-linux-x86_64.sh"
      d) Then, type "./cmake-3.26.0-linux-x86_64.sh", type "Y" until it has been successfully installed
      e) Go to the bin folder, use the "./ccmake --version" to check its version
      f) Rename foler cmake-3.26.0-linux-x86_64 as cmake-3.26.0
      g) Remove previous cmake by "module rm cmake/3.16.0"
      h) Use the new cmake. As the folder "cmake-3.26.0" is within the folder of "umesh-wald" and outside of "build" foler, type "../cmake-3.26.0/bin/ccmake ../"
      i) Remember to modify back the CMakeList.txt, replace "cmake_minimum_required(VERSION 3.10)" with "cmake_minimum_required(VERSION 3.16)", 3.16 is the original one
  4) After "../cmake-3.26.0/bin/ccmake ../", type "c" then "g"
  5) Within the "build" folder, type "make"
  6) Tetrahedralize by "./umeshTetrahedralize -o output_1.umesh input.umesh"
  7) WriteTS by "./writeTS -o output.ts output_1.umesh"
     Notes:
     a) Show the first 20 rows: head -n 20 output.ts
     b) Show the last 20 rows: tail -n 20 output.ts
