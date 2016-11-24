'''
Created on Oct 27, 2016

@author: akira
'''
import random, logging

import networkx as nx

logger = logging.getLogger(__name__)
POS_KEY = 'original'

class MiscException(Exception):
    pass

def dist_ring(source, target, size): # helper func
    if source >= size or target >= size:
        logger.debug("invalid args")
        raise MiscException
    
    return min(abs(source - target), size - abs(source - target))

def dist_lattice(p1, p2, size, dim=1):
    if type(p1) == int and dim == 1:
        return(dist_ring(p1, p2, size))

    if any([x >= size for x in p1]) or any([x >= size for x in p2]):
        logger.debug("invalid args")
        raise MiscException
    if dim == 1:
        return sum((min(abs(b-a), size-abs(b-a)) for a,b in zip(p1, p2)))
    else:
        return sum((abs(b-a) for a,b in zip(p1, p2))) 
    
def localcon_ring(node, size):
    if node == 0:
        return (size-1, 1)
    elif node == size-1:
        return (size-2, 0)
    else:
        return (node-1, node+1)

def localcon_lattice(node, size, dim=1):
    pass

def labels_from_attr(G, attr):        
    return dict((n,d.get(attr, '')) for n,d in G.nodes(data=True))

def switch_nodes(G, x, y):
    size = G.number_of_nodes()
    G.add_node(size) # temp
    # store x-edges
    ebunch = []
    for neigh in G.neighbors_iter(x):
        e = (size, neigh)
        G.add_edge(*e)
        ebunch.append((x, neigh))
    G.remove_edges_from(ebunch)
    
    # rewire x-edges
    ebunch = []
    for neigh in G.neighbors_iter(y):
        G.add_edge(*(x,neigh))
        ebunch.append((y, neigh))
    G.remove_edges_from(ebunch)
    
    # rewire y-edges
    for neigh in G.neighbors_iter(size):
        G.add_edge(*(y,neigh))
    G.remove_node(size)
    
    G.node[x][POS_KEY], G.node[y][POS_KEY] = G.node[y].get(POS_KEY, ''), G.node[x].get(POS_KEY, '') 

def shuffle_position_ring(G, iteration=None):
    G = G.copy()
    size = G.number_of_nodes()
    if not iteration:
        iteration = size
    # store original position
    for nd in G.nodes():
        G.node[nd][POS_KEY] = nd
    
    for _ in range(0, iteration):     
        n1 = int(random.uniform(0, size))
        n2 = int(random.uniform(0, size))
        logger.debug("switching %d and %d", n1, n2)
        switch_nodes(G, n1, n2)
        #G = nx.relabel_nodes(G, {n1:n2, n2:n1})
        
    labels = labels_from_attr(G, POS_KEY)
    
    return (G, labels)

def color_path(G, path, color='b', color_def='k', width=4.0, width_def=0.5):
    path_elist = [(path[i], path[i+1]) for i in range(0, len(path)-1)] # [(n0,n1), (n1,n2), ...]
    clist = []
    wlist = []
    logger.info(path_elist)
    for e in G.edges_iter():
        if e in path_elist or (e[-1], e[0]) in path_elist:
            clist.append(color)
            wlist.append(width)
        else:
            clist.append(color_def)
            wlist.append(width_def)
    return (clist, wlist)


