import os
import sys
import pickle
import json
from urllib.error import URLError

from scapy.all import traceroute
from urllib.request import urlopen
from database import Database
from model import Hop, Trace
from dotenv import load_dotenv


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
            "date_created": "unknown"
        }

    return json.loads(response_content.decode("utf-8"))


def main():
    db = Database()
    conn = db.get_connection()
    result, error = traceroute(sys.argv[1])
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
                date_created=geo_ip.get("current_time")
            )

        )

    trace.commit()
    inf = open(trace.id, "wb")
    pickle.dump(result, inf)
    inf.close()
    print(f"the trace is store as {trace.id}")


if __name__ == "__main__":
    load_dotenv()
    main()
