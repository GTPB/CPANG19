#!/usr/bin/python

import sys
from Gfa import *

ingraph = sys.argv[1]
outgraph = sys.argv[2]

graph = Graph()
graph.load(ingraph)

removed_nodes = []

for n in graph.nodes:
	fwpos = (n, True)
	bwpos = (n, False)
	single_node = True
	if len(graph.edges[fwpos]) != 0 or len(graph.edges[bwpos]) != 0:
		for t in graph.edges[fwpos]:
			if t[0][0] != n:
				single_node = False
				break
		for t in graph.edges[bwpos]:
			if t[0][0] != n:
				single_node = False
				break
	if not single_node: continue
	removed_nodes.append(n)

for n in removed_nodes:
	del graph.nodes[n]

graph.remove_nonexistent_edges()

graph.write(outgraph)
