import os, sys, argparse, logging, logging.handlers
from math import log

import networkx as nx

from utils.search import RoutingSimulator
from utils.search import mode_name_to_num

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

def fformat(value):
    return "%.15f" % value

def result_formatter(results): # [(size,min_deg,succ,apl),..]
    results = sorted(results)
    formatted = [] 
    for res in results:
        formatted.append(",".join([str(x) for x in res]))
    return formatted

def main(argv):
    parser = argparse.ArgumentParser(description="Freenet routing simulator")
    parser.add_argument("-v", "--verbose", action="count", default=0, dest="verbose",
                        help="Enable verbose output (specify multiple times to increase level)")
    parser.add_argument("-l", "--logfile", action="store", metavar="FILE", dest="logfile",
                        help="Log file name")
    parser.add_argument("-d", "--srcdir", action="store", metavar="DIR", dest="srcdir",
                        help="Source directory path")
    parser.add_argument("-s", "--suffix", action="store", default='', metavar="SUFFIX", dest="suffix",
                        help="Output file suffix")
    parser.add_argument("-m", "--mode", action="append", type=str, metavar="MODE", dest="modes", 
                        help="Specify routing algorithms to be used: FAIL, CONT, EVN, D2DFS, D3DFS, ALL")
    args = parser.parse_args(argv)
    
    # Logging setup
    logging_setup(args)
    logger = logging.getLogger('main')
        
    # parsing args
    if not args.srcdir:
        logger.error("input dir needs to be specified")
        return 1
    flist = [os.path.abspath(os.path.join(args.srcdir,x)) for x in os.listdir(args.srcdir)]
    logger.info("found following files: %s", flist)
       
    simulators = []
    if not args.modes or "ALL" in args.modes:
        simulators = [RoutingSimulator(x) for x in sorted(mode_name_to_num.values())]
    else:   
        for mode_str in args.modes:
            simulators.append(RoutingSimulator(mode_str))
    
    glist = []    
    try:
        for f in flist:
            glist.append(nx.read_graphml(f, node_type=float))
    except Exception as exc:
        logger.error("failed to read input file: %s", exc)
        return 1


    for sim in simulators:
        print("\n########### Running %s ###########" % sim.get_mode())
        results = []
        for G in glist:
            size = G.number_of_nodes()
            min_deg = sorted(nx.degree(G).values())[0]
            ttl = round(log(size, 2)**2)
            logger.info("size=%d, minimum deg=%d, TTL=%d", size, min_deg, ttl)
            srate, apl = sim.perform(G, show_progress=True)
            results.append((size, min_deg, srate, apl))
            print("\n")
    
        out = "{}{}.csv".format(sim.get_mode(), args.suffix)
        formatted = result_formatter(results)
        
        logger.info("writing results into %s", out)
        with open(out, 'a') as f:
            for l in formatted:
                f.write("{}\n".format(l))
        

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
