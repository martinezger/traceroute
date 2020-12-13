import os
import sys
from unittest.mock import patch, MagicMock
from urllib.error import URLError

from numpy.distutils.system_info import system_info
from six import BytesIO

import tracer
from database import Database
from tracer import geolocate_ip


class TestGeolocateIp:
    def setup(self):
        os.environ["API_KEY"] = "sample"

    def test_geolocate_ip__success(self):
        with patch("tracer.urlopen") as urlopen_patch:
            urlopen_patch.return_value = BytesIO(b'\n{"sample":"sample"}\n')
            result = geolocate_ip("192.168.1.1")

        expected_url = "https://api.ipgeolocation.io/ipgeo?apiKey=sample&ip=192.168.1.1"
        urlopen_patch.assert_called_once_with(expected_url)
        assert result == {"sample": "sample"}

    def test_geolocate_ip__error(self):

        with patch("tracer.urlopen") as urlopen_patch:
            urlopen_patch.side_effect = URLError("HTTP Error")
            result = geolocate_ip("192.168.1.1")

        expected_url = "https://api.ipgeolocation.io/ipgeo?apiKey=sample&ip=192.168.1.1"
        expected_response = {
            "country_name": "unknown",
            "city": "unknown",
            "isp": "unknown",
            "latitude": "unknown",
            "longitude": "unknown",
            "time_zone": {"current_time": ""},
        }
        urlopen_patch.assert_called_once_with(expected_url)
        assert result == expected_response


class TestMain:
    def setup_method(self, method):
        self.db = Database("test.sqlite")
        self.db.create_tables()

    @patch("tracer.Database")
    @patch("tracer.traceroute")
    @patch("tracer.geolocate_ip")
    @patch("tracer.pickle")
    @patch("tracer.open")
    def test_main__success(
        self, mock_open, mock_pickle, mock_geolocate_ip, mock_traceroute, mock_database
    ):
        mock_traceroute.return_value = ([MagicMock()], [MagicMock()])
        mock_database.return_value = self.db
        mock_geolocate_ip.return_value = {
            "country_name": "unknown",
            "city": "unknown",
            "isp": "unknown",
            "latitude": "unknown",
            "longitude": "unknown",
            "time_zone": {"current_time": ""},
        }

        tracer.main("www.example.com")

        mock_traceroute.assert_called_once_with("www.example.com")
        mock_database.assert_called_once()
        mock_geolocate_ip.assert_called_once()
        mock_pickle.dump.assert_called_once()
        mock_open.assert_called_once()
