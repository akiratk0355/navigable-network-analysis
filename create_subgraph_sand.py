'''
Created on Jan 6, 2017

@author: akira
'''
import copy, random

import networkx as nx
import numpy as np

G_default = nx.read_graphml("data/wot_default.graphml", node_type=int)
"""
# test graph
G = nx.Graph()
H = nx.path_graph(7)
G.add_nodes_from(H)
G.add_edges_from([(0,4),(0,6),(1,3),(1,4),(1,6),(2,4),(3,6),(4,5),(5,6)])
"""

indict = {}
for i in range(1,1000):
    indict[i]=[]

size = 10000
maxsize = 50000

while size < maxsize:
    gn = [41]
    safecount = 0
    percent = 0
    precision = 100
    if size >= 1000:
        precision = 1000
    if size >= 10000:
        precision = 10000
    
    while len(gn) < size and safecount < size + 100:
        cand = {}
        idct = copy.deepcopy(indict)
        inmax = 0
        div = size // precision
        if safecount % div == 0:
            print("creating wot{}: {}% done: reached {}".format(size, percent, safecount))
            percent += 100 / precision
        for nd in gn:
            for neigh in G_default.neighbors_iter(nd):
                if neigh in gn:
                    continue
                if cand.get(neigh):
                    imanoedge = cand[neigh]
                    cand[neigh] = imanoedge + 1
                    idct[imanoedge+1].append(neigh)
                    if inmax < imanoedge+1:
                        inmax = cand[neigh]
                else:
                    cand[neigh] = 1
                    idct[1].append(neigh)
                    if inmax == 0:
                        inmax = 1
        
        #print("current Gn = %s" % gn)
        #print("count=%d, %s" % (safecount, cand))
        #print(idct)
        #print("inmax=%d" % inmax)
        if inmax == 0:
            print("no more edges into Gn, aborting")
            break
        greatest = random.choice(idct[inmax])
        gn.append(greatest)
        
        safecount += 1
    
    G_new = nx.Graph(G_default.subgraph(gn))
    mapper = {}
    for i, nd in enumerate(G_new.nodes()):
        mapper[nd] = i + 50000
    G_new = nx.relabel_nodes(G_new, mapper)
    
    mapper = {}
    for i, nd in enumerate(G_new.nodes()):
        mapper[nd] = i
    G_new = nx.relabel_nodes(G_new, mapper)
    
    
    nx.write_graphml(G_new, "data/wot%d_default.graphml"%size)
    size += 2000

            
    
