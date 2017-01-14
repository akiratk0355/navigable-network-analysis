import logging, random, sys
from math import log

import numpy as np

from utils.misc import id_dist_ring, id_localcon_ring

logger = logging.getLogger(__name__)

SOURCE = -1

LOCAL = 10
FAIL = 1
CONT = 2
EVN = 3
D2DFS = 4
D3DFS = 5

mode_name_to_num = {
    #"LOCAL": LOCAL,
    "FAIL": FAIL,
    "CONT": CONT,
    "EVN": EVN,
    "D2DFS": D2DFS,
    "D3DFS": D3DFS
    }
mode_num_to_name = {v: k for k, v in mode_name_to_num.items()}

routingmode_opts = {
    #LOCAL: {"use_local": True},
    FAIL: {},
    CONT: {"strict": False},
    EVN: {"strict": False},
    D2DFS: {"strict": False, "backtrack": True},
    D3DFS: {"strict": False, "backtrack": True}
    }

class RoutingError(Exception):
    pass

class Node(object):
    def __init__(self, id):
        self.id = id
        self.visited = False
        self.predecessor = None
    
    def add_predecessor(self, node):
        self.predecessor = node
    
    def get_predecossor(self):
        return self.predecessor
    
    def mark(self):
        self.visited = True
    
    def is_visited(self):
        return self.visited

def greedy_path(G, source, target, ttl=None, deg_dict={},
                use_local=False, strict=True, backtrack=False):
    path = [source]
    curr = source
    hop = 0
    visited = {}
    pred_dict = {source:SOURCE}
    
    while not curr == target:
        visited[curr] = True
        curr_to_tgt = id_dist_ring(curr, target)
        logger.debug("current node is {0:.6f}: d({1:.6f}, {2:.6f})={3:.6f}".format(curr, curr, target, curr_to_tgt))
        if ttl and hop >= ttl:
            raise RoutingError("number of hops reached a limit %d, terminating" % ttl) 
        best = None
        best_to_tgt = 100 # dummy

        for neigh in G.neighbors(curr):
            if visited.get(neigh, False):
                continue
            d = id_dist_ring(neigh, target)
            logger.debug("checking neighbor {0:.6f}: d({1:.6f}, {2:.6f})={3:.6f}".format(neigh, neigh, target, d))
            if d/deg_dict.get(neigh,1.0) <= best_to_tgt:
                best = neigh
                best_to_tgt = d/deg_dict.get(neigh,1.0)                
        
        if curr_to_tgt < best_to_tgt:
            logger.debug("encountered dead-end at %f !", curr)
            if not strict:
                if best == None: # no unvisited neighbors
                    if backtrack and pred_dict[curr] == SOURCE:
                        raise RoutingError("terminating at dead-end node %f: source has touched all the neighbors" % curr)
                    elif backtrack:
                        best = pred_dict[curr]
                        logger.debug("node %f has no unvisited neighbors, returning to its predecessor %f", curr, best)
                    else:
                        logger.debug("node %f has no unvisited neighbors", curr)
                        raise RoutingError("terminating at dead-end node %f: no unvisited neighbors" % curr)
                else:
                    pred_dict[best] = curr
                    logger.debug("using the second best node %f", best)
            elif use_local:
                ndlist = sorted(G.nodes())
                pre, suc = id_localcon_ring(ndlist, curr)
                if id_dist_ring(pre, target) < id_dist_ring(suc, target):
                    best = pre
                else:
                    best = suc
                pred_dict[best] = curr
                logger.debug("using local connection %f", best)
            else:
                raise RoutingError("terminating at dead-end node %f: no nodes closer to the target" % curr) 
        else:
            pred_dict[best] = curr
        # move on to next node
        hop += 1
        path.append(best)
        curr = best
        
    logger.debug("routing succeeded after %d steps!!", hop)
    logger.debug("pred_dict=%s", pred_dict)
    visited[target] = True
    return (path, visited, hop)

class SimulationResult(object):
    def __init__(self, mode, size, srate, apl, core=None):
        self.mode = mode
        self.size = size
        self.srate = srate
        self.apl = apl
        self.core = core

class RoutingSimulator(object):
    def __init__(self, mode, trial_per_src=5):
        self.trial_per_src = trial_per_src
        self.results = []
        try:
            if type(mode) == str:
                self.mode = mode_name_to_num[mode]
            else:
                self.mode = mode
            self.opts = routingmode_opts[self.mode]
        except KeyError:
            logger.error("undefined routing mode %s", mode)
            raise
    
    def get_mode(self, num=False):
        if not num:
            return mode_num_to_name[self.mode]
        return self.mode
    
    def perform(self, G, show_progress=False, save_result=False):
        succ_hops = []
        success = 0
        size = G.number_of_nodes()
        ttl = round(log(size, 2)**2)
        percent = 0
        precision = 100
        if size > 7000:
            precision = 1000

        div = size//precision
    
        deg_dict = {}
        ndlist = sorted(G.nodes())
        if self.mode == EVN or self.mode == D3DFS:
            for nd in G.nodes():
                deg_dict[nd] = G.degree(nd)
        
        logger.info("performing routing simulation in mode %s\n    ttl=%d\n    network size=%d", 
                    self.get_mode(), ttl, size)
        for i, src in enumerate(ndlist):
            if show_progress and i % div == 0:
                sys.stdout.write("\r{0:.2f}% done: reached {1:d}/{2:d}".format(percent, i, size))
                sys.stdout.flush()
                percent += 100 / precision
            for _ in range(0, self.trial_per_src):
                dst = random.choice(ndlist)
                while dst == src: # we luckily chose the same id, try again 
                    dst = random.choice(ndlist)
                
                #print("finding path from %s to %s" % (src, dst))
                try:
                    path, vstd, hop = greedy_path(G, src, dst, ttl=ttl, deg_dict=deg_dict,
                                                   **self.opts)
                except RoutingError:
                    #print("failed")
                    continue
                else:
                    succ_hops.append(hop)
                    success += 1
        
        sys.stdout.write("\nsimulation done \n")
        sys.stdout.flush()
        srate = success/(size*self.trial_per_src)
        apl = np.average(succ_hops)
        logger.info("\n    SUCC = %.3f\n    AHOPS = %.3f", srate, apl)
        if save_result:
            self.results.append(SimulationResult(self.mode, size, srate, apl))
        return (srate, apl)
