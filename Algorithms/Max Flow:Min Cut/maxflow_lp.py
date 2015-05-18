# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 14:39:03 2014

@author: Jordan
"""

import sys
import networkx as nx
from pulp import *
file = sys.argv[1]
source = int(sys.argv[2])
sink = int(sys.argv[3])
G = nx.read_gml(file)



prob = LpProblem("MaxFlow_LP",LpMaximize)


edges={}
ins = {k: [] for k in G.nodes_iter()}

for (i,j) in G.edges_iter():
    edges[(i,j)] = LpVariable(str(i)+"->"+str(j), 0, 1, LpInteger)
    edges[(j,i)] = LpVariable(str(j)+"->"+str(i), 0, 1, LpInteger)
    ins[j].append(i)
    ins[i].append(j)

out=ins

    
prob += lpSum(edges[source,j] for j in out[source]), "Total Flow"

for v in G.nodes_iter():
    if v != source and v != sink:        
        prob += (lpSum([edges[i,v] for i in ins[v]]) == lpSum([edges[v,i] for i in out[v]])), "Flow Conservation %s"%v
    if v == sink:
        prob += (lpSum([edges[i,v] for i in ins[v]]) == lpSum([edges[source,i] for i in out[source]])), "Flow Conservation %s"%v
    if v == source:
        prob += (lpSum([edges[i,v] for i in ins[v]]) == 0), "Flow Conservation %s"%v
        
prob.solve()
#print LpStatus[prob.status]
print int(value(prob.objective))
