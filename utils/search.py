import logging, random
from math import sqrt

import numpy as np

from utils.misc import dist_lattice, id_dist_ring, id_localcon_ring


logger = logging.getLogger(__name__)

class RoutingError(Exception):
    pass

def greedy_path(G, source, target, dim=1, cutoff=None, use_local=False, strict=True, deg_dict={}):
    path = [source]
    curr = source
    step = 0
    visited = {}
    
    while not curr == target:
        visited[curr] = True
        curr_to_tgt = id_dist_ring(curr, target)
        logger.debug("current node is %d: d(%d, %d)=%d", curr, curr, target, curr_to_tgt)
        if cutoff and step >= cutoff:
            raise RoutingError("number of hops reached a limit %d, terminating" % cutoff) 
        best = None
        best_to_tgt = 100 # dummy

        for neigh in G.neighbors(curr):
            if visited.get(neigh, False):
                continue
            d = id_dist_ring(neigh, target)
            logger.debug("checking neighbor %d: d(%d, %d)=%d", neigh, neigh, target, d)
            if d/deg_dict.get(neigh,1.0) <= best_to_tgt:
                best = neigh
                best_to_tgt = d/deg_dict.get(neigh,1.0)                
        
        if curr_to_tgt < best_to_tgt:
            logger.debug("encountered dead-end at %d !", curr)
            if not strict:
                if best == None: # no unvisited neighbors
                    logger.debug("node %d has no unvisited neighbors", curr)
                    raise RoutingError("terminating at dead-end node %d: no unvisited neighbors" % curr)
                else:
                    logger.debug("using the second best node %d", best)
            elif use_local:
                ndlist = sorted(G.nodes())
                pre, suc = id_localcon_ring(ndlist, curr)
                if id_dist_ring(pre, target) < id_dist_ring(suc, target):
                    best = pre
                else:
                    best = suc
                logger.debug("using local connection %d", best)
            else:
                raise RoutingError("terminating at dead-end node %d: no nodes closer to the target" % curr) 
                
        # move on to next node
        step += 1
        path.append(best)
        curr = best
        
    logger.debug("routing succeeded after %d steps!!", step)
    visited[target] = True
    return (path, visited, step)

def average_greedy_path_length(G, trial_per_src=5, debug=False, cutoff=None, use_local=False, strict=True, use_deg=False):
    lsum = 0
    success = 0
    size = G.number_of_nodes()
    percent = 0
    div = size//100

    deg_dict = {}
    ndlist = sorted(G.nodes())
    if use_deg:
        for nd in G.nodes():
            deg_dict[nd] = G.degree(nd)
        
    for i, src in enumerate(ndlist):
        if debug and i % div == 0:
            logger.info("{}% done: reached {}".format(percent, i))
            percent += 1
        for _ in range(0, trial_per_src):
            dst = random.choice(ndlist)
            while dst == src: # we luckily chose the same id, try again 
                dst = random.choice(ndlist)
            
            #print("finding path from %s to %s" % (src, dst))
            try:
                path, vstd, step = greedy_path(G, src, dst, cutoff=cutoff, use_local=use_local, strict=strict, deg_dict=deg_dict)
            except RoutingError:
                #print("failed")
                continue
            else:
                lsum += step
                success += 1
    return (lsum/success, success/(size*trial_per_src))
