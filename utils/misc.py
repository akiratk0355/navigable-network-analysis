'''
Created on Oct 27, 2016

@author: akira
'''

class MiscException(Exception):
    pass

def dist_ring(source, target, size): # helper func
    if source >= size or target >= size:
        print("invalid args")
        raise MiscException
    
    return min(abs(source - target), size - abs(source - target))
    
