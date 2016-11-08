'''
Created on Oct 27, 2016

@author: akira
'''
import networkx as nx
from bisect import bisect_left
import random

from .misc import dist_ring

def kleinberg_ring(n, p=1, q=1, r=1, seed=None):
    if (p < 0):
        raise nx.NetworkXException("p must be >= 0")
    if (q < 0):
        raise nx.NetworkXException("q must be >= 0")
    if (r < 0):
        raise nx.NetworkXException("r must be >= 1")
    if not seed is None:
        random.seed(seed)
    G = nx.Graph()
    nodes = [x for x in range(0, n)]
    for p1 in nodes:
        probs = [0]
        for p2 in nodes:
            if p1==p2:
                continue
            d = dist_ring(p1, p2, len(nodes))
    
            if d <= p:
                G.add_edge(p1,p2)
                #print("local contact %s to %s" % (p1, p2))
            probs.append(d**-r)
        cdf = list(nx.utils.accumulate(probs))
        for _ in range(q):
            idx = bisect_left(cdf,random.uniform(0, cdf[-1]))
            target = nodes[idx]
            if idx >= p1:
                target += 1            
            G.add_edge(p1,target)
            #print("long-range contact %s to %s" % (p1, target))
    return G
