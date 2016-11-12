import logging, random

from .misc import dist_ring, localcon_ring

logger = logging.getLogger(__name__)

class RoutingError(Exception):
    pass

def greedy_path(G, source, target, cutoff=None, use_local=False, strict=True):
    path = [source]
    curr = source
    step = 0
    visited = {}
    size = G.number_of_nodes()
    while not curr == target:
        visited[curr] = True
        curr_to_tgt = dist_ring(curr, target, size)
        logger.debug("current node is %d: d(%d, %d)=%d", curr, curr, target, curr_to_tgt)
        if cutoff and step >= cutoff:
            raise RoutingError("number of hops reached a limit %d, terminating" % cutoff) 
        best = None
        best_to_tgt = size # dummy

        for neigh in G.neighbors(curr):
            if visited.get(neigh, False):
                continue
            d = dist_ring(neigh, target, size)
            logger.debug("checking neighbor %d: d(%d, %d)=%d", neigh, neigh, target, d)
            if d <= best_to_tgt:
                best = neigh
                best_to_tgt = d
        
        if curr_to_tgt <= best_to_tgt:
            logger.debug("encountered dead-end at %d !", curr)
            if not strict:
                if best == None: # no unvisited neighbors
                    logger.debug("node %d has no unvisited neighbors", curr)
                    raise RoutingError("terminating at dead-end node %d: no unvisited neighbors" % curr)
                else:
                    logger.debug("using the second best node %d", best)
            elif use_local:
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

def average_greedy_path_length(G, iteration=10000, cutoff=None, use_local=False, strict=True):
    lsum = 0
    success = 0
    for _ in range(0, iteration):
        src = int(random.uniform(0,G.number_of_nodes()))
        dst = int(random.uniform(0,G.number_of_nodes()))
        #print("finding path from %s to %s" % (src, dst))
        try:
            path, vstd, step = greedy_path(G, src, dst, cutoff=cutoff, use_local=use_local, strict=strict)
        except RoutingError:
            #print("failed")
            continue
        else:
            lsum += step
            success += 1
    
    return (lsum/success, success/iteration)