'''
Created on Oct 27, 2016

@author: akira
'''
import random, logging

import networkx as nx
import numpy as np

logger = logging.getLogger(__name__)

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
    nx.relabel_nodes(G, {x:2}, copy=False)
    nx.relabel_nodes(G, {y:x}, copy=False)
    nx.relabel_nodes(G, {2:y}, copy=False)
    """
    temp = -1.0
    G.add_node(temp) # temp
    # store x-edges
    ebunch = []
    for neigh in G.neighbors_iter(x):
        if neigh == y:
            continue
        e = (temp, neigh)
        G.add_edge(*e)
        ebunch.append((x, neigh))
    G.remove_edges_from(ebunch)
    
    # rewire x-edges
    ebunch = []
    for neigh in G.neighbors_iter(y):
        if neigh == x:
            continue
        G.add_edge(*(x,neigh))
        ebunch.append((y, neigh))
    G.remove_edges_from(ebunch)
    
    # rewire y-edges
    for neigh in G.neighbors_iter(temp):
        G.add_edge(*(y,neigh))
    G.remove_node(temp)
    """

def shuffle_position_ring(G, iteration=None):
    G = G.copy()
    ndlist = G.nodes()
    size = G.number_of_nodes()
    if not iteration:
        iteration = size * 100
    
    for _ in range(0, iteration):
        x = random.choice(ndlist)
        y = random.choice(ndlist)
        logger.debug("switching %d and %d", x, y)
        switch_nodes(G, x, y)
    
    return G

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

def frac_local_contact(G):
    size = G.number_of_nodes()
    num = 0
    ndlist = sorted(G.nodes())
    for i, nd in enumerate(ndlist):
        if i == size - 1:
            if G.has_edge(nd, ndlist[0]):
                num += 1
        elif G.has_edge(nd, ndlist[i+1]):
            num += 1
    return num/size

def id_dist_ring(id1, id2):
    return min(abs(id1 - id2), 1.0 - abs(id1 - id2))

def id_localcon_ring(ndlist, node):
    idx = ndlist.index(node)
    if idx == 0:
        return (ndlist[-1], ndlist[1])
    elif idx == len(ndlist) - 1:
        return (ndlist[-2], ndlist[0])
    else:
        return (ndlist[idx-1], ndlist[idx+1])

def id_assign_random(G):
    mapper = {}
    for nd in G.nodes():
        mapper[nd] = np.random.ranf()
    G = nx.relabel_nodes(G, mapper)
    return G

# takes a graph int ID and map to [0,1) ID space 
def id_assign_ordered(G):
    mapper = {}
    size = G.number_of_nodes()
    for nd in G.nodes():
        mapper[nd] = nd / size
    G = nx.relabel_nodes(G, mapper)
    return G

def ordered_circular_layout(G, scale=1.,center=None):
    if len(G) == 0:
        return {}
    nodes = np.array(sorted(G.nodes()))
    twopi = 2.0*np.pi
    theta = nodes*twopi
    pos = np.column_stack([np.cos(theta), np.sin(theta)]) * scale
    if center is not None:
        pos += np.asarray(center)

    return dict(zip(nodes, pos))

def draw_autocrop(plt, pos):
    cut = 1.2
    xmax= cut*max(xx for xx,yy in pos.values())
    ymax= cut*max(yy for xx,yy in pos.values())
    plt.xlim(-xmax,xmax)
    plt.ylim(-ymax,ymax)

def write_custom(G, path, encoding='utf-8', prettyprint=True):
    G = nx.OrderedGraph(G)
    nx.write_graphml(G, path, encoding, prettyprint)
