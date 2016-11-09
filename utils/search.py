import random

from .misc import dist_ring, localcon_ring

class RoutingError(Exception):
    pass

def greedy_path(G, source, target, cutoff=None, use_local=False, allow_back=False):
    path = [source]
    curr = source
    step = 0
    size = G.number_of_nodes()
    while not curr == target:
        step += 1
        curr_to_tgt = dist_ring(curr, target, size)
        #print("current node is %s" % curr)
        if cutoff and step > cutoff:
            #print("number of hops reached a limit, terminating")
            raise RoutingError() 
        best = curr
        best_to_tgt = dist_ring(best, target, size)

        for neigh in G.neighbors(curr):
            d = dist_ring(neigh, target, size)
            #print("checking neghbor %s, d(%s, %s)=%s" % (neigh, neigh, target, d))
            if d <= best_to_tgt:
                best = neigh
                best_to_tgt = d
        
        if curr_to_tgt == best_to_tgt:
            #print("encountered dead-end at %d!" % curr) 
            if use_local:
                pre, suc = localcon_ring(curr, size)
                if dist_ring(pre, target, size) < dist_ring(suc, target, size):
                    best = pre
                else:
                    best = suc
                #print("using local connection to %d" % best)
                
            else:
                #print("terminating!")
                raise RoutingError() 
                
            
        curr = best
        
        path.append(best)
            

    return path

def average_greedy_path_length(G, iteration=10000, cutoff=None, use_local=False, allow_back=False):
    lsum = 0
    success = 0
    for _ in range(0, iteration):
        src = int(random.uniform(0,G.number_of_nodes()))
        dst = int(random.uniform(0,G.number_of_nodes()))
        #print("finding path from %s to %s" % (src, dst))
        try:
            path = greedy_path(G, src, dst, cutoff=cutoff, use_local=use_local, allow_back=allow_back)
        except RoutingError:
            #print("failed")
            continue
        else:
            lsum += len(path) - 1
            success += 1
    
    return (lsum/success, success/iteration)