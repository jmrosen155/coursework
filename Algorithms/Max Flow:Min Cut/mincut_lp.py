# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 14:39:28 2014

@author: Jordan
"""

import sys
import networkx as nx
from pulp import *
file = sys.argv[1]
source = int(sys.argv[2])
sink = int(sys.argv[3])
G = nx.read_gml(file)


prob = LpProblem("MinCut_LP",LpMinimize)


q={}
p={} 

for (i,j) in G.edges_iter():
    q[(i,j)] = LpVariable(str(i)+"->"+str(j), 0, 1, LpInteger)
    q[(j,i)] = LpVariable(str(j)+"->"+str(i), 0, 1, LpInteger)

for v in G.nodes_iter():
    p[v] = LpVariable(str(v), 0, 1, LpInteger)


prob += lpSum(q[i,j] for (i,j) in q), "Min Cut with capacity=1"


for (i,j) in G.edges_iter():
    prob += (p[j]-p[i] <= q[i,j]), "Constraint"+str(j)+"-"+str(i)
    prob += (p[i]-p[j] <= q[j,i]), "Constraint"+str(i)+"-"+str(j)


prob += (p[sink]-p[source] == 1), "Source/Sink Diff Sets"


prob.solve()
#print LpStatus[prob.status]
print int(value(prob.objective))