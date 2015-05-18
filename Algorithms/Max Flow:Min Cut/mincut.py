# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 14:38:42 2014

@author: Jordan
"""

import sys
import networkx as nx
file = sys.argv[1]
source = int(sys.argv[2])
sink = int(sys.argv[3])
G = nx.read_gml(file)
for edge in G.edges_iter():
    G[edge[0]][edge[1]]['capacity'] = 1
min_cut = nx.minimum_cut_value(G,source,sink)
print(min_cut)