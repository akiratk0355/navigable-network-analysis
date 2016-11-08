from .misc import dist_ring

def greedy_path(G, source, target, cutoff=None):
    path = [source]
    curr = source
    step = 0
    while not curr == target:
        step += 1
        #print("current node is %s" % curr)
        if cutoff and step > cutoff:
            print("number of hops reached a limit, terminating")
            break
        best = curr
        best_to_tgt = dist_ring(best, target, G.number_of_nodes())

        for neigh in G.neighbors(curr):
            d = dist_ring(neigh, target, G.number_of_nodes())
            #print("checking neghbor %s, d(%s, %s)=%s" % (neigh, neigh, target, d))
            if d <= best_to_tgt:
                best = neigh
                best_to_tgt = d
        curr = best
        
        path.append(best)
            

    return path
