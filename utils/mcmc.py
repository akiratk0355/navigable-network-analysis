'''
Created on Jan 7, 2017

@author: akira
'''

import logging, random, sys

import networkx as nx
import numpy as np

from utils.misc import dist_ring, switch_nodes, id_dist_ring

logger = logging.getLogger(__name__)

DIST_SCALE = 5 # 5 is optimal?

def randomwalk(G, src, ttl=6):
    curr = src
    while ttl > 0:
        curr = random.choice(G.neighbors(curr))
        ttl -= 1

    if curr == src:
        return randomwalk(G, src)
    
    return curr

# helper func for swap
def distance_prod(G, x, y, switched=False, debug=False):
    prod = 1.0
    if debug:
        print("%f has neighbors=%s" % (x, G.neighbors(x)))
        print("%f has neighbors=%s" % (y, G.neighbors(y)))
    if not switched:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= id_dist_ring(x,ngh)*DIST_SCALE
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= id_dist_ring(y,ngh)*DIST_SCALE
    else:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= id_dist_ring(y,ngh)*DIST_SCALE
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= id_dist_ring(x,ngh)*DIST_SCALE
    
    return prod

def distance_prod_divfirst(G, x, y, debug=False):
    prod = 1.0
    
    bunbo = []
    bunshi = []
    xneigh = G.neighbors(x)
    yneigh = G.neighbors(y)
    
    common = list(set.intersection(set(xneigh), set(yneigh)))
    for c in common:
        xneigh.remove(c)
        yneigh.remove(c)
    
    # not switched
    for ngh in xneigh:
        if ngh == y:
            continue
        bunshi.append(id_dist_ring(x,ngh))
    for ngh in yneigh:
        if ngh == x:
            continue
        bunshi.append(id_dist_ring(y,ngh))
    
    # switched
    for ngh in xneigh:
        if ngh == y:
            continue
        bunbo.append(id_dist_ring(y,ngh))
    for ngh in yneigh:
        if ngh == x:
            continue
        bunbo.append(id_dist_ring(x,ngh))
    
    bunbo = sorted(bunbo)
    bunshi = sorted(bunshi)
    if not len(bunbo) == len(bunshi):
        raise
    
    for i in range(0, len(bunbo)):
        prod *= bunshi[i]/bunbo[i]
    
    if debug:
        print("bunshi=%s" % bunshi)
        print("bunbo=%s" % bunbo)
    
    return prod

def mh_swap(G, mcs, precision=1000, random_walk=True):
    percent = 0
    div = mcs // precision
    G = G.copy()
    ndlist = sorted(G.nodes())
    for i in range(0, mcs):
        if i % div == 0:
            sys.stdout.write("{}% done: reached {}/{}".format(percent, i, mcs))
            sys.stdout.flush()
            percent += 100 / precision
        x = random.choice(ndlist)
        y = random.choice(ndlist)
        if random_walk:
            y = randomwalk(G, x)
        else:
            while x == y:
                y = random.choice(ndlist)

        try:
            #cn = distance_prod(G,x,y)/distance_prod(G,x,y,switched=True)
            cn = distance_prod_divfirst(G, x, y)
            #print("%.15f" % cn2)
        except Exception as exc:
            print(exc)
            bb = distance_prod(G,x,y,switched=True, debug=True)
            print("%.15f" % bb)
            cn = 1.0
        acceptance = min(1.0, cn)
        #print("acceptance=%s" % acceptance)
        if np.random.ranf() < acceptance:
            #print("switching %d and %d" % (x,y))
            switch_nodes(G, x, y)
        else:
            #print("rejected switching %d and %d" % (x,y))
            pass
    sys.stdout.write("\nswapping done \n")
    sys.stdout.flush()
    return G
