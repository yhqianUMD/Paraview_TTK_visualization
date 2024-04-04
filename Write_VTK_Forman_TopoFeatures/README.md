# Visualize_D1_final.ipynb is used for writing descending 1-manifold and critical points to vtk files in pyspark

When saving critical points:
- write critical vertices
- write critical edges
- write critical triangles

When saving descending 1-manifolds:
- the vertices involved are those vertices along the V1-paths
- the edges connecting every VE pair along the V1-paths

# Visualize_A1_final.ipynb is used for writing ascending 1-manifold to vtk files in pyspark

When saving ascending 1-manifolds:
- the points involved are the mid-points of edges in ET pairs and barycenters of triangles in ET pairs
- the edges involved are the edges connecting the above points

# Visualize_gradient_final.ipynb is used for writing gradient vector to vtk files in pyspark

When saving the gradient vectors:
- the vertices stored:
  1. all regular vertices and critical vertices, which are equal to all the vertices in a mesh
  2. the mid-points of edges involved in ET pairs, the mid-points of critical edges are not included
  3. the barycenters of critical triangles are not included
- the triangles stored:
  all the triangles involved in ET pairs, critical triangles are not included
- vertices vector:
  1. for regular vertices: the difference between the mid-point of the paired edge and the current vertex in VE pair
  2. for critical vertices: the vector is [0, 0, 0]
- edges vector:
  only vectors of edges that are involved in ET pairs are included, critical edges are not considered
