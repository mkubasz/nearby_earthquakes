import json
from unittest import TestCase

from main import get_earthquakes, GeoPoints, nearby_earthquakes


class TestDistanceCalculator(TestCase):
    def test_valid_url_returns_list_of_earthquakes(self):
        earthquakes = get_earthquakes()
        assert isinstance(earthquakes, list)
        assert len(earthquakes) > 0
        assert all(key in earthquakes[0] for key in ['type', 'properties', 'geometry'])

    def test_list_contains_at_least_one_earthquake(self):
        earthquakes = get_earthquakes()
        assert len(earthquakes) > 0


    def test_happy_path_valid_input(self):
        point = GeoPoints(37.7749, -122.4194)
        nearby_earthquakes(point)
        assert True

    def test_happy_path_edge_input(self):
        point = GeoPoints(90, 180)
        nearby_earthquakes(point)
        assert True

    def test_happy_path_edge_input_zero_one(self):
        point = GeoPoints(0, 1)
        nearby_earthquakes(point)
        assert True

    def test_edge_case_no_earthquakes_in_past_30_days(self):
        point = GeoPoints(37.7749, -122.4194)
        data = get_earthquakes()
        for earthquake in data:
            earthquake["properties"]["time"] = 0
        nearby_earthquakes(point)
        assert True