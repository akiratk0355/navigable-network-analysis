'''
Created on Oct 27, 2016

@author: akira
'''
import networkx as nx
from bisect import bisect_left
import random

from .misc import dist_ring

# TODO: fix
def navigable_small_world_ring(n, p=1, q=1, r=1, seed=None):

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
            probs.append(d**-r)
        cdf = list(nx.utils.accumulate(probs))
        for _ in range(q):
            target = nodes[bisect_left(cdf,random.uniform(0, cdf[-1]))]
            G.add_edge(p1,target)
    return G
