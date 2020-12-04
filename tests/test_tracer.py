import os
from unittest.mock import patch
from urllib.error import URLError

from six import BytesIO

from tracer import geolocate_ip


class TestGeolocateIp:

    def setup(self):
        os.environ['API_KEY'] = 'sample'

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
        }
        urlopen_patch.assert_called_once_with(expected_url)
        assert result == expected_response
