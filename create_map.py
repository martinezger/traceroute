from scapy.all import *
import pickle
import sys


if "__main__" == __name__:
    conf.geoip_city = sys.argv[1]
    ofn = open(sys.argv[2], 'rb')
    trace = pickle.load(ofn)
    ofn.close()
    try:
        trace.world_trace()
    except Exception:
        print("quit")
