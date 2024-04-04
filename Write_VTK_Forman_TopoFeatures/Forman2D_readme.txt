critical_vertexes: its length is equal to the number of vertices. critical vertices are set as 0, others are set as -1

new_vertexes_triangles: its length is equal to the number of critical triangles. storing the baricenter point of critical triangles as xyz coordinate

edges: its length is equal to the number of edges in a mesh. storing the edges in a mesh as a map, where key is the edge and value is the mid-point of this edge

tri_baricenter: its length is equal to the number of triangles in a mesh. storing the baricenter of each triangle

vectors_gradient: its length is equal to the number of vertices. storing the gradient vector of VE pairs or critical vertices

new_vertexes: its length is equal to the sum of critical edges and edges involved in ET pairs. storing the mid-points of each edge, specifically, they are edges paired with triangles or critical edges; the edges paired with vertices are not included

new_vectors: its length is equal to new_vertexes. storing the gradient vector of ET pairs or critical edges

from_edges: its length is equal to new_vertexes. for ET pairs, it is -1; for critical edges, it is 1

for critical vertices, critical edges, and critical triangles, its gradient vector is (0,0,0)


For the descending 1 CELLS
vertici: vertices along V1-paths
edges: edges along V1-paths, including the critical edges
edge_number: the number of edges along V1-paths, including critical edges
vertex_number: the number of vertices along V1-paths

For the ascending 1 CELLS
edges: the edges connecting critical edges and critical triangles. Specifically, each edge connect the mnid-point of an edge and the baricenter of a triangle
vertices: the unique vertices along the edges
sortedVertices: the unique vertices along the edges in ascending order
