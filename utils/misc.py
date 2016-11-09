'''
Created on Oct 27, 2016

@author: akira
'''
import random

import networkx as nx

class MiscException(Exception):
    pass

def dist_ring(source, target, size): # helper func
    if source >= size or target >= size:
        print("invalid args")
        raise MiscException
    
    return min(abs(source - target), size - abs(source - target))
    
def localcon_ring(node, size):
    if node == 0:
        return (size-1, 1)
    elif node == size-1:
        return (size-2, 0)
    else:
        return (node-1, node+1)

def shuffle_position_ring(G, iteration=None):
    size = G.number_of_nodes()
    if not iteration:
        iteration = size
    # store original position
    for nd in G.nodes():
        G.node[nd]['original'] = nd
    
    for _ in range(0, iteration):     
        n1 = int(random.uniform(0, size))
        n2 = int(random.uniform(0, size))
        #print("switching %d and %d" % (n1, n2))
        G = nx.relabel_nodes(G, {n1:n2,n2:n1})
        
    labels = dict((n,d['original']) for n,d in G.nodes(data=True))
    
    return (G, labels)
        


