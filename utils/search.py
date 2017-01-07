import logging, random
from math import sqrt

from .misc import dist_ring, localcon_ring
from utils.misc import dist_lattice


logger = logging.getLogger(__name__)

class RoutingError(Exception):
    pass

def greedy_path(G, source, target, dim=1, cutoff=None, use_local=False, strict=True, use_deg=False):
    path = [source]
    curr = source
    step = 0
    visited = {}
    size = G.number_of_nodes()
    if dim == 2:
        size = int(sqrt(G.number_of_nodes()))
    
    while not curr == target:
        visited[curr] = True
        curr_to_tgt = dist_lattice(curr, target, size, dim=dim)
        logger.debug("current node is %d: d(%d, %d)=%d", curr, curr, target, curr_to_tgt)
        if cutoff and step >= cutoff:
            raise RoutingError("number of hops reached a limit %d, terminating" % cutoff) 
        best = None
        best_to_tgt = size * dim# dummy
        best_to_tgt_withdeg = best_to_tgt

        for neigh in G.neighbors(curr):
            if visited.get(neigh, False):
                continue
            d = dist_lattice(neigh, target, size, dim=dim)
            logger.debug("checking neighbor %d: d(%d, %d)=%d", neigh, neigh, target, d)
            if not use_deg:
                if d <= best_to_tgt:
                    best = neigh
                    best_to_tgt = d
            else:
                if d/G.degree(neigh) <= best_to_tgt_withdeg:
                    best = neigh
                    best_to_tgt = d
                    best_to_tgt_withdeg = d / G.degree(neigh)
        
        if curr_to_tgt <= best_to_tgt:
            logger.debug("encountered dead-end at %d !", curr)
            if not strict:
                if best == None: # no unvisited neighbors
                    logger.debug("node %d has no unvisited neighbors", curr)
                    raise RoutingError("terminating at dead-end node %d: no unvisited neighbors" % curr)
                else:
                    logger.debug("using the second best node %d", best)
            elif use_local: #TODO: support use_local for dim == 2
                pre, suc = localcon_ring(curr, size)
                if dist_ring(pre, target, size) < dist_ring(suc, target, size):
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

def average_greedy_path_length(G, trial_per_src=5, cutoff=None, use_local=False, strict=True, use_deg=False):
    lsum = 0
    success = 0
    size = G.number_of_nodes()
    for src in range(0, size):
        for _ in range(0, trial_per_src):
            dst = int(random.uniform(0,size))
            while dst == src: # we luckily chose the same id, try again 
                dst = int(random.uniform(0,size))
            
            #print("finding path from %s to %s" % (src, dst))
            try:
                path, vstd, step = greedy_path(G, src, dst, cutoff=cutoff, use_local=use_local, strict=strict, use_deg=use_deg)
            except RoutingError:
                #print("failed")
                continue
            else:
                lsum += step
                success += 1
    return (lsum/success, success/(size*trial_per_src))
