import os
import sys
import pickle
import json
from urllib.error import URLError
from urllib.request import urlopen
from scapy.layers.inet import TracerouteResult, traceroute

from database import Database
from model import Hop, Trace
from dotenv import load_dotenv


def save_to_file(result: TracerouteResult, trace: Trace):

    if not os.path.exists('traces'):
        os.makedirs('traces')

    inf = open(f"traces/{trace.id}", "wb")
    pickle.dump(result, inf)
    inf.close()
    print(f"the trace is store as {trace.id}")



def geolocate_ip(ip: str) -> dict:
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={os.getenv('API_KEY')}&ip={ip}"
    try:
        with (urlopen(url)) as response:
            response_content = response.read()
    except URLError as e:
        print(e)
        return {
            "country_name": "unknown",
            "city": "unknown",
            "isp": "unknown",
            "latitude": "unknown",
            "longitude": "unknown",
            "time_zone": {"current_time": ""},
        }

    return json.loads(response_content.decode("utf-8"))


def main(host):
    db = Database()
    conn = db.get_connection()
    result, error = traceroute(host)
    trace = Trace(conn)
    hops = []
    for i, hop in enumerate(result):
        geo_ip = geolocate_ip(hop[1].src)
        trace.add(
            Hop(
                hop=i + 1,
                ip=hop[1].src,
                country_name=geo_ip.get("country_name"),
                city=geo_ip.get("city"),
                isp=geo_ip.get("isp"),
                latitude=geo_ip.get("latitude"),
                longitude=geo_ip.get("longitude"),
                date_created=geo_ip.get("time_zone").get("current_time"),
            )
        )

    trace.commit()
    save_to_file(result, trace)

if __name__ == "__main__":
    load_dotenv()
    main(host=sys.argv[1])
