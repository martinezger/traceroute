import os
import sys
import pickle
import json
from urllib.error import URLError

from scapy.all import traceroute
from urllib.request import urlopen
from database import Database
from model import Hop, Trace

API_KEY = os.getenv('API_KEY', 'sample')


def geolocate_ip(ip: str) -> dict:
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}"
    try:
        with (urlopen(url)) as response:
            response_content = response.read()
    except URLError as e:
        print(e)
        return {'country_name': 'unknown', 'city': 'unknown', 'latitude': 'unknown', 'longitude': 'unknown'}

    return json.loads(response_content.decode('utf-8'))


def main():
    db = Database()
    conn = db.get_connection()
    result, error = traceroute(sys.argv[1])
    trace = Trace(conn)
    hops = []
    for i, hop in enumerate(result):
        geo_ip = geolocate_ip(hop[1].src)
        trace.add(Hop(hop=i + 1, ip=hop[1].src, **geo_ip))

    trace.commit()
    inf = open(trace.id, 'wb')
    pickle.dump(result, inf)
    inf.close()
    print(f"the trace is store as {trace.id}")


if __name__ == "__main__":
    main()



