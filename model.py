from datetime import datetime
from uuid import uuid4

from dataclasses import dataclass


@dataclass
class Hop:
    hop: int
    ip: str
    country_name: str
    city: str
    isp: str
    latitude: float
    longitude: float
    date_created: datetime

    def __str__(self):
        return (
            f"HOP:{self.hop}, IP:{self.ip},  COUNTRY:{self.country_name}, CITY:{self.city}, "
            f"ISP:{self.isp}, LATITUDE:{self.latitude}, LONGITUDE:{self.longitude}, DATE_CREATED:{self.date_created}"
        )


class Trace:
    def __init__(self, conn):
        self.conn = conn
        self.id = uuid4().__str__()
        self.hops = []

    def add(self, hop: Hop) -> None:
        self.hops.append(
            (
                self.id,
                hop.hop,
                hop.ip,
                hop.country_name,
                hop.city,
                hop.isp,
                hop.latitude,
                hop.longitude,
                hop.date_created
            )
        )

        return f"New hop {hop}"

    def commit(self) -> str:
        sql = """INSERT INTO TRACE  (ID, HOP, IP, COUNTRY, CITY, ISP, LATITUDE, LONGITUDE, DATE_CREATED)
                 VALUES (?,?,?,?,?,?,?,?,?)"""
        try:
            for hop in self.hops:
                self.conn.execute(sql, hop)
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)
            return

        return "all traces are commit"
