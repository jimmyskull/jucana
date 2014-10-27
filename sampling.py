# -*- coding: utf-8 -*-
# Leskovec, J. & Faloutsos, C. Sampling from large graphs.import In Proc. of 
# the 12th ACM SIGKDD International Conference on Knowledge Discovery and 
# Data Mining, 631–636 (ACM, 2006).

from random import choice, uniform

import igraph

TELEPORTATION_FACTOR = 0.15
MAX_VERTICES = 1000
MAX_EDGES = 7000

vertices = set()
edges = set()

g = igraph.read('debatenaglobo_graph.net', format='pajek')

# Random walk (see paper)
v_id = choice(g.vs).index
while len(vertices) < MAX_VERTICES or len(edges) < MAX_EDGES:
    next = choice(g.vs[v_id].neighbors()).index
    edges.add(frozenset((v_id, next)))
    vertices.add(next)
    v_id = next
    if uniform(0, 1) <= TELEPORTATION_FACTOR:
        v_id = choice(g.vs).index
    print '\r{}%'.format(len(edges) * 100.0 / MAX_EDGES),

# Clean-up
edge_list = list()
vertex_list = list()
for v in g.vs:
    if v.index not in vertices:
        vertex_list.append(v.index)

for e in g.get_edgelist():
    if frozenset(e) not in edges:
        edge_list.append(e)

g.delete_edges(edge_list)
g.delete_vertices(vertex_list)

r = igraph.power_law_fit(g.degree())

# Output
g.write_pajek('sampled_graph.net')

print 'Sampling graph'
print 'Vertices: {}'.format(len(vertices))
print 'Edges: {}'.format(len(edges))
print 'Power law alpha: {}'.format(r.alpha)

