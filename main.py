import os
import json
import logging
import argparse

import requests
from datetime import datetime, timedelta
from geopy import distance
from dataclasses import dataclass


@dataclass
class GeoPoints:
    """
    A class that represents a point in the Earth.
    """
    lat: float
    lon: float

    def latlon(self) -> tuple[float, float]:
        """
        Returns the latitude and longitude of the point.
        """
        return self.lat, self.lon

    @staticmethod
    def __int__(self, lat: float, lon: float) -> 'GeoPoints':
        """
        Creates a GeoPoint object with the given latitude and longitude.

        Args:
          lat: The latitude of the point.
          lon: The longitude of the point.

        Returns:
          A GeoPoint object.
        """
        # Validate the latitude and longitude values.

        if not -90 <= lat <= 90:
            raise Exception("Invalid latitude value: {}".format(lat))
        if not -180 <= lon <= 180:
            raise Exception("Invalid longitude value: {}".format(lon))
        if lat == lon:
            raise Exception("Latitude and longitude cannot be the same")

        self.lat = float(lat)
        self.lon = float(lon)


EARTHQUAKE_URL = os.environ.get('EARTHQUAKE_URL', "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")
MAX_DISTANCE = 5000
def logger_builder():
    """
    Creates a logger and configures it to log to a file.

    Returns:
      The logger.
    """

    # Create a logger.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler and set the log level.
    file_handler = logging.FileHandler('earthquake.log')
    file_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the file handler.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger.
    logger.addHandler(file_handler)
    return logger


Log = logger_builder()


def get_earthquakes() -> list[dict]:
    """
    Gets a list of earthquakes from the USGS Earthquake Hazards Program.

    Returns:
      A list of dictionaries, each of which contains information about an earthquake.
    """

    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    response = requests.get(url)
    if response.status_code != 200:
        Log.error("Error fetching earthquakes: {}".format(response.status_code))
        raise Exception("Error fetching earthquakes: {}".format(response.status_code))
    data = json.loads(response.content)
    return data["features"]


def get_distance(point: GeoPoints, point2: GeoPoints) -> float:
    """Returns the distance between two points in kilometers."""
    return round(distance.distance(point.latlon(), point2.latlon()).kilometers)


def is_after_days(time: float) -> bool:
    """
    Returns True if the given time is after 30 days, False otherwise.

    Args:
      time: The time in milliseconds since the Unix epoch.

    Returns:
      True if the time is after 30 days, False otherwise.
    """

    time = datetime.fromtimestamp(time / 1000)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    return time > thirty_days_ago


def nearby_earthquakes(point: GeoPoints) -> None:
    """
    Gets the 10 most nearby earthquakes to the given latitude and longitude.

    Args:
        point
    Returns:
      Nothing.
    """

    # Get a list of earthquakes.
    earthquakes = get_earthquakes()

    # Filter the earthquakes to only include those that happened after 30 days.

    nearby_earthquakes = []
    for earthquake in earthquakes:
        if not is_after_days(earthquake["properties"]["time"]):
            continue

        # Get the title, latitude, longitude, and distance of each earthquake.

        title = earthquake["properties"]["title"]
        lat = earthquake["geometry"]["coordinates"][1]
        lon = earthquake["geometry"]["coordinates"][0]

        distance = get_distance(point, GeoPoints(lat, lon))

        # Add the earthquake to the list of nearby earthquakes if it is within 1000 kilometers.

        if distance < MAX_DISTANCE:
            nearby_earthquakes.append((title, distance))

    # Sort the list of nearby earthquakes by distance.

    nearby_earthquakes.sort(key=lambda x: x[1])

    # Print the 10 most nearby earthquakes.

    for title, distance in nearby_earthquakes[:10]:
        print("{} || {}".format(title, distance))
        Log.info("{} || {}".format(title, distance))


if __name__ == "__main__":
    try:

        parser = argparse.ArgumentParser()
        parser.add_argument('-lat', type=float, required=True, help='Latitude')
        parser.add_argument('-lon', type=float, required=True, help='Longitude')

        args = parser.parse_args()
        point = GeoPoints(args.lat, args.lon)
        nearby_earthquakes(point)
    except ValueError:
        Log.error("Invalid latitude or longitude value")
        raise Exception("Invalid latitude or longitude value")
