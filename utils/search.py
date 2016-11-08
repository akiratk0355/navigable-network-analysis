from .misc import dist_ring, localcon_ring

def greedy_path(G, source, target, cutoff=None, skip_local=False):
    path = [source]
    curr = source
    step = 0
    size = G.number_of_nodes()
    while not curr == target:
        step += 1
        curr_to_tgt = dist_ring(curr, target, size)
        #print("current node is %s" % curr)
        if cutoff and step > cutoff:
            print("number of hops reached a limit, terminating")
            break
        best = curr
        best_to_tgt = dist_ring(best, target, size)

        for neigh in G.neighbors(curr):
            d = dist_ring(neigh, target, size)
            #print("checking neghbor %s, d(%s, %s)=%s" % (neigh, neigh, target, d))
            if d <= best_to_tgt:
                best = neigh
                best_to_tgt = d
        
        if curr_to_tgt == best_to_tgt:
            print("encountered dead-end at %d!" % curr)
            if skip_local:
                pre, suc = localcon_ring(curr, size)
                if dist_ring(pre, target, size) < dist_ring(suc, target, size):
                    best = pre
                else:
                    best = suc
                print("using local connection to %d" % best)
                
            else:
                print("terminating!")
                return path
                
            
        curr = best
        
        path.append(best)
            

    return path
