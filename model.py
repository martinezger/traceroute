from uuid import uuid4

from dataclasses import dataclass


@dataclass
class Hop:
    hop: int
    ip: str

    def __str__(self):
        return f"HOP:{self.hop}, IP:{self.ip}"


class Trace:

    def __init__(self, conn):
        self.conn = conn
        self.id = uuid4().__str__()
        self.hops = []

    def insert(self, hop: Hop) -> str:
        self.hops.append(
         (self.id, hop.hop, hop.ip)
        )

        return f" New hop {hop.__str__()}"

    def commit(self):
        sql = "INSERT INTO TRACE  (ID, HOP, IP) VALUES (?,?,?)"
        try:
            for hop in self.hops:
                self.conn.execute(sql, hop)
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)
            return

        return "all traces are commit"
