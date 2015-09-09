import json
import unittest
import mock
import requests

import urbanairship as ua


class TestLocationFinder(unittest.TestCase):
    def setUp(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "features": [{
                "bounds": [
                    37.63983,
                    -123.173825,
                    37.929824,
                    -122.28178
                ],
                "centroid": [
                    37.759715,
                    -122.693976
                ],
                "id": "4oFkxX7RcUdirjtaenEQIV",
                "properties": {
                    "boundary_type": "city",
                    "boundary_type_string": "City/Place",
                    "context": {
                        "us_state": "CA",
                        "us_state_name": "California"
                    },
                    "name": "San Francisco",
                    "source": "tiger.census.gov"
                },
                "type": "Feature"
            }]
        }).encode('utf-8')
        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [mock_response]
        airship = ua.Airship('key', 'secret')
        self.l = ua.LocationFinder(airship)

    def test_name_lookup(self):
        info = self.l.name_lookup('name')
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_name_lookup_with_type(self):
        info = self.l.name_lookup('name', 'type')
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_coordinates_lookup(self):
        info = self.l.coordinates_lookup(123, 123)
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_coordinates_lookup_with_type(self):
        info = self.l.coordinates_lookup(123, 123, 'type')
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_invalid_coordinates(self):
        self.assertRaises(
            TypeError,
            callableObj=self.l,
            latitude='123',
            longitude=123
        )

    def test_bounding_box_lookup(self):
        info = self.l.bounding_box_lookup(123, 123, 123, 123)
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_bounding_box_lookup_with_type(self):
        info = self.l.bounding_box_lookup(123, 123, 123, 123, 'type')
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_invalid_bounding_box(self):
        self.assertRaises(
            TypeError,
            callableObj=self.l.bounding_box_lookup,
            lat1='123',
            long1=123,
            lat2=123,
            long2=123
        )

    def test_alias_lookup(self):
        info = self.l.alias_lookup('alias=alias')
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_alias_list_lookup(self):
        info = self.l.alias_lookup(['alias=alias1', 'alias=alias2'])
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_polygon_lookup(self):
        info = self.l.polygon_lookup('id', 1)
        self.assertEqual(info['features'][0]['bounds'], [37.63983, -123.173825, 37.929824, -122.28178])

    def test_invalid_zoom(self):
        self.assertRaises(
            TypeError,
            callableObj=self.l.polygon_lookup,
            polygon_id='id',
            zoom='1'
        )
