import sys
import pickle
from scapy.all import traceroute

from database import Database
from model import Hop, Trace


if __name__ == "__main__":

    db = Database()
    conn = db.get_connection()
    result, error = traceroute(sys.argv[1])
    trace = Trace(conn)
    hops = []
    for i, hop in enumerate(result):
        trace.insert(Hop(i+1, hop[1].src))

    trace.commit()
    inf = open(trace.id, 'wb')
    pickle.dump(result, inf)
    inf.close()
    print(f"the trace is store as {trace.id}")



