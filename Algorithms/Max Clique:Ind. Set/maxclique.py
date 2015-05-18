# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:39:11 2014

@author: Jordan
"""

import sys
import networkx as nx
from pulp import *
file = sys.argv[1]
G = nx.read_gml(file)
H = nx.complement(G)


prob = LpProblem("MaxClique_IP",LpMaximize)

x = {}
for v in G.nodes_iter():
    x[v] = LpVariable(str(v), 0, 1, LpInteger)

prob += lpSum(x[v] for v in G.nodes_iter()), "Maximize Clique"

for (i,j) in H.edges_iter():
    prob += (x[i]+x[j] <= 1), "Constraint"+str(i)+"-"+str(j)
    
prob.solve(solver=pulp.COIN_CMD())
print int(value(prob.objective))

#print nx.graph_clique_number(G)