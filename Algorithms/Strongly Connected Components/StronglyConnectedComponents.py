# Algorithms for Data Science
# HW2 - Programming
# Jordan Rosenblum


def readinput(file):       #Reads input into an adjacency list - G and G_rev
    file = 'InputGraphs/' + file   
    a = open(file, 'r')
    b = a.readline()
    n, m = [int(z) for z in b.split()]
    G = {}
    G_rev = {}
    for i in xrange(1,n+1):
        G[i] = []
        G_rev[i] = []
    for line in a:
        temp1, temp2 = line.split()
        temp1 = int(temp1)
        temp2 = int(temp2)
        if temp2 not in G[temp1]:
            G[temp1].append(temp2)
        if temp1 not in G_rev[temp2]:
            G_rev[temp2].append(temp1)
    a.close()
    return n, m, G, G_rev
    
def DFS(G, order):               #Runs Depth First Search on Graph G and finds the forest of trees  
    global i
    global forest
    forest = []
    i = 0
    for u in order:
        explored[u] = 0
    for u in order:
        if explored[u] == 0:
            forest.append([])            
            search(G, u)
            i += 1

def search(G, u):             #Searches a node of Graph G
    global time
    global forest
    start[u] = time
    time += 1
    explored[u] = 1
    forest[i].append(u)
    for v in order:
        if v in G[u]:
            if explored[v] == 0:
                search(G, v)
    finish[u] = time
    time += 1
  
def writeoutput(SCC, file):      #Writes the SCC to the output text files
    file = 'OutputGraphs/' + file   
    a = open(file, 'w')
    a.write(str(len(SCC)) + '\n')
    temp = [[ int(j) for j in i] for i in SCC ]
    for comp in sorted(temp, key=min):
        a.write(str(len(comp)) + ' ')
        temp1 = sorted(comp)
        temp1 = [ str(x) for x in temp1 ]
        a.write(' '.join(temp1))
        a.write('\n')
    a.close()


for j in xrange(20):          #Code iterating through each of the 20 input files
    time = 1
    i = 0
    explored = {}
    start = {}
    finish = {}
    forest = []
    if len(str(j)) == 1:
        file = 'in0' + str(j) + '.txt'
    else:
        file = 'in' + str(j) + '.txt'
    n, m, G, G_rev = readinput(file)
    order = sorted(G.keys())
    DFS(G, order)
    order = sorted(finish, key=finish.get, reverse=True)
    DFS(G_rev, order)
    SCC = forest
    fileout = 'out' + file[2:4] + '.txt'
    writeoutput(SCC, fileout)
