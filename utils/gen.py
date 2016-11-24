'''
Created on Oct 27, 2016

@author: akira
'''
from bisect import bisect_left
from itertools import product
import random, logging

import networkx as nx

from .misc import dist_ring, dist_lattice

logger = logging.getLogger(__name__)

def kleinberg_ring(n, p=1, q=1, r=1, seed=None):
    if (p < 0):
        raise nx.NetworkXException("p must be >= 0")
    if (q < 0):
        raise nx.NetworkXException("q must be >= 0")
    if (r < 0):
        raise nx.NetworkXException("r must be >= 0")
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
                logger.debug("local contact %s to %s", p1, p2)
            probs.append(d**-r)
        cdf = list(nx.utils.accumulate(probs))
        for _ in range(q):
            idx = bisect_left(cdf,random.uniform(0, cdf[-1]))
            if idx <= p1:
                idx -= 1
            target = nodes[idx]
            G.add_edge(p1,target)
            logger.debug("long-range contact %s to %s", p1, target)
    return G

def kleinberg(n, p=1, q=1, r=2, dim=2, seed=None):
    if (p < 0):
        raise nx.NetworkXException("p must be >= 0")
    if (q < 0):
        raise nx.NetworkXException("q must be >= 0")
    if (r < 0):
        raise nx.NetworkXException("r must be >= 0")
    if not seed is None:
        random.seed(seed)
    G = nx.Graph()
    nodes = list(product(range(n), repeat=dim))
    for i, p1 in enumerate(nodes):
        probs = [0]
        for p2 in nodes:
            if p1==p2:
                continue
            d = dist_lattice(p1, p2, n, dim=dim)
            if d <= p:
                if dim == 1:
                    G.add_edge(p1[0], p2[0])
                else:
                    G.add_edge(p1,p2)
                logger.debug("local contact %s to %s", p1, p2)
            probs.append(d**-r)
        cdf = list(nx.utils.accumulate(probs))
        for _ in range(q):
            idx = bisect_left(cdf,random.uniform(0, cdf[-1]))
            if idx <= i:
                idx -= 1
            target = nodes[idx]
            if dim == 1:
                G.add_edge(p1[0], target[0])
            else:
                G.add_edge(p1,target)
            logger.debug("long-range contact %s to %s", p1, target)
        
    return G
