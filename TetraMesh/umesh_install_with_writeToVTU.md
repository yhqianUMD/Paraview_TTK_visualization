# The following are techniques for converting a tetrahedral mesh to a VTU file

1. git clone from https://gitlab.com/ingowald/umesh
   '''
   git clone https://gitlab.com/ingowald/umesh.git
   '''
2. create a folder
   '''
   cd umesh
   mkdir build
   cd build
   '''
3. ccmake
   '''
   /local/data/yuehui/local_yh/cmake-3.23.0/bin/ccmake ../
   '''
   Then, press 'c' for configure; if we encountered an error of "TBB not found", we can ignore it and continue press 'c'; Next, change the following setting during ccmake:
   * Change “CMAKE_INSTALL_PREFIX” to your local directory instead of “/usr/local”, e.g., “/local/data/yuehui/local_yh/umesh_03252025/umesh-install”.
   * Set “UMESH_USE_TBB” to “OFF” (TBB is optional dependency for parallelizing some routines).
   * Set “UMESH_USE_VTK” to “ON”
   * if cmake cannot find the VTK_DIR, you can manually set it to the path under ParaView (like what we did when we installed TTK). e.g., "nano CMakeCache.txt", and add "VTK_DIR:PATH=/local/data/yuehui/local_yh/ttk-env/lib/cmake/vtk-9.2"
4. install
   '''
   make
   '''
