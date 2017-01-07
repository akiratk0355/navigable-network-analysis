'''
Created on Jan 6, 2017

@author: akira
'''

from math import log
import random, os, sys, argparse, logging, logging.handlers

import networkx as nx
import numpy as np

from utils.misc import dist_ring, switch_nodes

def logging_setup(args):
    log_root = logging.getLogger('')
    if args.verbose > 1:
        log_root.setLevel(logging.DEBUG)
    elif args.verbose == 1:
        log_root.setLevel(logging.INFO)
    
    log_format = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    log_handler = logging.StreamHandler()
    if args.logfile:
        log_handler = logging.handlers.WatchedFileHandler(args.logfile, encoding='utf-8')
    log_handler.setFormatter(log_format)
    log_root.addHandler(log_handler)

def distance_prod(G, x, y, size, switched=False):
    prod = 1.0
    #print("neighbors=%s" % G.neighbors(x))
    #print("neighbors=%s" % G.neighbors(y))
    if not switched:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= dist_ring(x,ngh,size)
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= dist_ring(y,ngh,size)
    else:
        for ngh in G.neighbors(x):
            if ngh == y:
                continue
            prod *= dist_ring(y,ngh,size)
        for ngh in G.neighbors(y):
            if ngh == x:
                continue
            prod *= dist_ring(x,ngh,size)
    
    return prod

def main(argv):
    parser = argparse.ArgumentParser(description="Embedding simulator with location swapping")
    parser.add_argument("-v", "--verbose", action="count", default=0, dest="verbose",
                        help="Enable verbose output (specify multiple times to increase level)")
    parser.add_argument("-d", "--debug", action="count", default=0, dest="debug",
                        help="Enable debugging mode")
    parser.add_argument("-l", "--logfile", action="store", metavar="FILE", dest="logfile",
                        help="Log file name")
    parser.add_argument("-f", "--srcfile", action="store", metavar="FILE", dest="srcfile",
                        help="Source file path")
    parser.add_argument("-o", "--outfile", action="store", metavar="FILE", dest="outfile",
                        help="Output file path")
    parser.add_argument("-s", "--srcstr", action="append", metavar="STRING", dest="srcstr",
                        help="Source strings")
    parser.add_argument("-m", "--mode", action="store", type=int, metavar="MODENUM", default=0, dest="mode", 
                        help="Mode number")
    parser.add_argument("-i", "--iterations", action="store", type=float, metavar="ITERNUM", default=6000, dest="iters",
                        help="Number of iterations per node (default to 6000)")
    args = parser.parse_args(argv)
    
    # Logging setup
    logging_setup(args)
    logger = logging.getLogger('main')
    
    logger.info("running in mode %d", args.mode)
    
    # parsing args
    if not args.srcfile:
        logger.error("input file needs to be specified")
        return 1
    infile = os.path.abspath(args.srcfile)
    
    outfile = infile + ".emb"
    if args.outfile:
        outfile = os.path.abspath(args.outfile)
    
    if args.srcstr:
        logger.debug("received strings: %s",  args.srcstr)
        # do_something(args.srcstr)
    
    try:
        G = nx.read_graphml(infile, node_type=int)
    except Exception as exc:
        logger.error("failed to read input file: %s", exc)
        return 1
    
    # start
    n = G.number_of_nodes()
    max_step = int(log(n, 2))*int(log(n, 2))
    logger.info("n=%s, max step=%s", n, max_step)
    
    mcs = int(args.iters*n)
    precision = 1000
    logger.info("running %d mcs...", mcs)
    percent = 0
    for i in range(0, mcs):
            div = mcs / precision
            if i % div == 0:
                logger.info("{}% done: reached {}".format(percent, i))
                percent += 100 / precision
            x = int(random.uniform(0,n))
            y = int(random.uniform(0,n))
            #print("trying x-y switch: (%s,%s)" % (x,y))
            acceptance = min(1.0, distance_prod(G,x,y,n)/distance_prod(G,x,y,n,switched=True))
            #print("acceptance=%s" % acceptance)
            if random.uniform(0,1) < acceptance:
                #print("switching %d and %d" % (x,y))
                switch_nodes(G, x, y)
            else:
                #print("rejected switching %d and %d" % (x,y))
                pass
    
    logger.info("writing result to %s", outfile)
    nx.write_graphml(G, outfile)
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

