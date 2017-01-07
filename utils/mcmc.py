'''
Created on Jan 7, 2017

@author: akira
'''

import random, logging

import networkx as nx
import numpy as np

from utils.misc import dist_ring, switch_nodes

logger = logging.getLogger(__name__)

# helper func for swap
def distance_prod(G, x, y, size, switched=False):
    prod = 1.0
    #print("neighbors=%s" % G.neighbors(x))
    #print("neighbors=%s" % G.neighbors(y))
    if not switched:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= dist_ring(x,ngh,size)
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= dist_ring(y,ngh,size)
    else:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= dist_ring(y,ngh,size)
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= dist_ring(x,ngh,size)
    
    return prod

def mh_swap(G, mcs, precision=1000, random_walk=False):
    percent = 0
    n = G.number_of_nodes()
    G = G.copy()
    for i in range(0, mcs):
        div = mcs / precision
        if i % div == 0:
            logger.info("{}% done: reached {}".format(percent, i))
            percent += 100 / precision
        x = np.random.randint(0,n)
        y = np.random.randint(0,n)
        if random_walk:
            pass
        #print("trying x-y switch: (%s,%s)" % (x,y))
        acceptance = min(1.0, distance_prod(G,x,y,n)/distance_prod(G,x,y,n,switched=True))
        #print("acceptance=%s" % acceptance)
        if np.random.rand() < acceptance:
            #print("switching %d and %d" % (x,y))
            switch_nodes(G, x, y)
        else:
            #print("rejected switching %d and %d" % (x,y))
            pass
    return G
