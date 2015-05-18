# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 23:53:00 2014

@author: Jordan
"""

#pulp.COIN_CMD().available()
#pulp.pulpTestAll()


import sys
import networkx as nx
from pulp import *
file = sys.argv[1]
G = nx.read_gml(file)


def method1():        #max ind set using networkx function
    x=[]
    for i in xrange(10):
        temp = len(nx.maximal_independent_set(G))
        print(temp)
        x.append(temp)
    print max(x)


def method2():        #max ind set using integer program
    prob = LpProblem("MaxIS_IP",LpMaximize)

    x = {}
    for v in G.nodes_iter():
        x[v] = LpVariable(str(v), 0, 1, LpInteger)

    prob += lpSum(x[v] for v in G.nodes_iter()), "Maximize IS"

    for (i,j) in G.edges_iter():
        prob += (x[i]+x[j] <= 1), "Constraint"+str(i)+"-"+str(j)
    
    prob.solve(solver=pulp.COIN_CMD())
    print int(value(prob.objective))

def method3():        #max ind set using relaxed linear program
    prob = LpProblem("MaxIS_LP",LpMaximize)

    x = {}
    for v in G.nodes_iter():
        x[v] = LpVariable(str(v), 0, 1)

    prob += lpSum(x[v] for v in G.nodes_iter()), "Maximize IS"

    for (i,j) in G.edges_iter():
        prob += (x[i]+x[j] <= 1), "Constraint"+str(i)+"-"+str(j)
    
    prob.solve()
    print value(prob.objective)
    
    
method1()
method2()
method3()