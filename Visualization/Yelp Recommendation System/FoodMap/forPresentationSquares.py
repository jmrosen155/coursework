
# coding: utf-8

# In[81]:

import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np

plt.clf()
plt.cla()
plt.close()

mpl.rcParams['lines.linewidth'] = 1.25
fig = plt.gcf()
fig.set_size_inches(10.5,10.5)

# Parameters
data = [118,109,70,68,65,56,56,53,42,41,40,39,36,36,36,30,30,30,25,25,25,25,20,20,20,20,20,15,15,15,15,10,10,10,5,5,5,5] 
maxV = max(data)
data = [i * 180.0/maxV for i in data] 
frame = [600, 600]
center = [0, 0]
margin = 2
plt.ylim([-325,325])
plt.xlim([-325,325])

# Anonymous functions
f = lambda x: x[0]**2 + x[1]**2

# Positioning
plt.plot([300,300],[-300,300],'k-')
plt.plot([-300,-300],[-300,300],'k-')
plt.plot([300,-300],[300,300],'k-')
plt.plot([300,-300],[-300,-300],'k-')
plt.plot([0,0],[-300,300],'k-')
plt.plot([300,-300],[0,0],'k-')

# Model Setting
global quads, margin, sqrs
quads = {0: {'centers':[(0,0)]},
         1: {'centers':[(0,0)]},
         2: {'centers':[(0,0)]},
         3: {'centers':[(0,0)]}}
sqrs  = {0: [],
         1: [],
         2: [],
         3: []}

# Plot funcntion
def drawSquare(L,q,thisPoint = None):
    global quads, margin, sqrs
    if thisPoint:
        ptIdx = quads[q]['centers'].index(thisPoint)
        centers = quads[q]['centers'].pop(ptIdx)
    else:
        centers = quads[q]['centers'].pop(0)
    if q == 0:
        uX = centers[0] + margin
        uY = centers[1] + margin + L
        #plt.scatter(uX,uY,s=75,c='r')
        #plt.scatter(uX+L,uY-L,s=75,c='r')
        quads[q]['centers'].extend([(centers[0]+L+2*margin,centers[1]),(centers[0],centers[1]+L+2*margin)])
    elif q == 1:
        uX = centers[0] + margin
        uY = centers[1] - margin
        #plt.scatter(uX,uY-L,s=75,c='r')
        #plt.scatter(uX+L,uY,s=75,c='r')
        quads[q]['centers'].extend([(centers[0]+L+2*margin,centers[1]),(centers[0],centers[1]-L-2*margin)])
    elif q == 2:
        uX = centers[0] - L - margin
        uY = centers[1] - margin
        #plt.scatter(uX,uY,s=75,c='r')
        #plt.scatter(uX+L,uY-L,s=75,c='r')
        quads[q]['centers'].extend([(centers[0]-L-2*margin,centers[1]),(centers[0],centers[1]-L-2*margin)])
    elif q == 3:
        uX = centers[0] - L - margin
        uY = centers[1] + L + margin
        #plt.scatter(uX,uY-L,s=75,c='r')
        #plt.scatter(uX+L,uY,s=75,c='r')
        quads[q]['centers'].extend([(centers[0]-L-2*margin,centers[1]),(centers[0],centers[1]+L+2*margin)])
    sqrs[q].append(((uX,uY),(uX+L,uY-L))) 
    plt.plot([uX,uX],[uY,uY-L],'b-')
    plt.plot([uX+L,uX+L],[uY,uY-L],'b-')
    plt.plot([uX,uX+L],[uY,uY],'b-')
    plt.plot([uX,uX+L],[uY-L,uY-L],'b-')
    return True

# Checking if squares overlap
def checkOverlap(thisSquare, q):
    ((l1x,l1y),(r1x,r1y)) = thisSquare
    global quads, margin, sqrs
    for ((l2x,l2y),(r2x,r2y)) in sqrs[q]:
        if (l1x > r2x or l2x > r1x) or (l1y < r2y or l2y < r1y):
            continue
        else:
            return False
    return True

# Find optimal location to place the square based on euclidian distance
def optPoint(quads):
    tmp = []
    for q in quads.keys():
        vList = [(q,x,f(x)) for x in quads[q]['centers']]
        tmp.extend(vList)
    minV = min(tmp, key = lambda (q,x,v):v)
    return [tup for idx, tup in enumerate(tmp) if tup[2] == minV[2]][0] #Pick the first point, need to fix later

def optPoint2(quads,L,margin):
    tmp = []
    for q in quads.keys():
        vList = [(q,x,f(x)) for x in quads[q]['centers']]
        tmp.extend(vList)
    sortedTmp = sorted(tmp, key=lambda  x:x[2])
    #print sortedTmp
    for thisRow in sortedTmp:
        q = thisRow[0]
        centers = thisRow[1]
        if q == 0:
            uX = centers[0] + margin
            uY = centers[1] + margin + L
        elif q == 1:
            uX = centers[0] + margin
            uY = centers[1] - margin
        elif q == 2:
            uX = centers[0] - L - margin
            uY = centers[1] - margin
        elif q == 3:
            uX = centers[0] - L - margin
            uY = centers[1] + L + margin
        thisSquare = ((uX,uY),(uX+L,uY-L))
        if checkOverlap(thisSquare, q):
            return thisRow
        #return thisRow
    return None
        
# first four squares
for q in xrange(4):
    L = data.pop(0)
    drawSquare(L,q)
    
for L in data:
    a = optPoint2(quads,L,margin)
    if a:
        drawSquare(L,a[0],a[1])
    else:
        break

#fig.savefig('backFill.png',dpi=100)
plt.show()


# In[27]:

xFrame = frame[0]
yFrame = frame[1]

res = []
for q in sqrs.keys():
    for pts in sqrs[q]:
        ((uX,uY),(bX,bY)) = pts
        L = abs(uX - bX)
        fX = uX + xFrame/2
        if uY >= 0:
            fY = yFrame/2 - uY
        else: 
            fY = yFrame/2 + abs(uY)
        res.append(((fX,fY),L))        

res = sorted(res, key=lambda x:x[1], reverse=True)
tmp = []
for r in res:
    tmp.append(((r[0][1],r[0][0]),r[1]))
tmp
#import json
#a = {}
#for i in xrange(len(res)):
#    a[i] = {}
#    ((x_axis,y_axis),size) = res[i]
#    a[i]['x_axis'] = x_axis
#    a[i]['y_axis'] = y_axis
#    a[i]['size'] = size

#for key in a.keys():
#    if key == sorted(a.keys())[0]:
#        print '[{"y_axis": %f, "x_axis": %f, "size": %f},' % (a[key]['y_axis'],a[key]['x_axis'],a[key]['size'])
#    elif key == sorted(a.keys())[-1]:
#        print '{"y_axis": %f, "x_axis": %f, "size": %f}];' % (a[key]['y_axis'],a[key]['x_axis'],a[key]['size'])
#    else:
#        print '{"y_axis": %f, "x_axis": %f, "size": %f},' % (a[key]['y_axis'],a[key]['x_axis'],a[key]['size'])        
#print json.dumps(a, indent=4)


# In[ ]:




# In[ ]:




# In[ ]:



