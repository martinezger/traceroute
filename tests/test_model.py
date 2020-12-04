from unittest.mock import MagicMock

import pytest

from database import Database
from model import Hop, Trace


class TestHop:
    def test_hop__instantiation(self):
        hop = Hop(1, "19.19.19.19", "Argentina", "Barranqueras", 12.12, 11.11)

        assert (
            str(hop)
            == f"HOP:{hop.hop}, IP:{hop.ip},  COUNTRY:{hop.country_name}, CITY:{hop.city}, "
            f"LATITUDE:{hop.latitude}, LONGITUDE:{hop.longitude}"
        )


class TestTrace:
    def test_trace__add__hop(self):
        hop = Hop(1, "19.19.19.19", "Argentina", "Barranqueras", 12.12, 11.11)
        trace = Trace(Database("test.sqlite").get_connection())
        result = trace.add(hop)

        assert trace.id
        assert trace.conn
        assert len(trace.hops) == 1
        assert result == f"New hop {hop}"

    def test_trace__commit_success(self):
        db = Database("test.sqlite")
        db.create_tables()
        hop = Hop(1, "19.19.19.19", "Argentina", "Barranqueras", 12.12, 11.11)
        trace = Trace(db.get_connection())
        trace.add(hop)
        result = trace.commit()
        from_db = db.get_connection().execute("select * from trace").fetchall()
        assert from_db
        assert result == "all traces are commit"

    @pytest.mark.skip("review why exception is not working")
    def test_trace__commit_exception(self):

        conn = MagicMock()
        conn.commit.side_effect = Exception()

        hop = Hop(1, "19.19.19.19", "Argentina", "Barranqueras", 12.12, 11.11)
        trace = Trace(conn)
        trace.add(hop)

        with pytest.raises(Exception):
            trace.commit()
