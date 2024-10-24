import xarray as xr
import numpy as np
from .const import EARTH_RADIUS, DEFAULT_TOPO_DIR
import json
import os
import logging

logger = logging.getLogger(__name__)


def _haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points on the Earth (specified in decimal degrees).

    returns:
        Distance (in meters)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    m = EARTH_RADIUS * c
    return m


def _get_relative_altitude(
    lat: float, lon: float, *, radius: float = 5000, altitude: float, topography_file
):
    topo = xr.open_dataset(topography_file)

    distances = _haversine(topo["lon"], topo["lat"], lon, lat)

    within_radius = distances <= radius

    values_within_radius = topo["Band1"].where(within_radius, drop=True)

    min_value = float(values_within_radius.min())

    return altitude - max([min_value, 0])


def _get_topo_file_for_coord(
    lat: float, lon: float, *, topodir: str = DEFAULT_TOPO_DIR
) -> str:
    with open(os.path.join(topodir, "metadata.json")) as f:
        data = json.load(f)

    for file in data:
        if lat < data[file]["s"] or lat > data[file]["n"]:
            continue
        if lon < data[file]["w"] or lon > data[file]["e"]:
            continue

        return os.path.join(topodir, file)

    raise ValueError(f"Not topography data found for lat={lat:.2f};lon={lon:.2f}")


def get_relative_altitude(
    lat: float,
    lon: float,
    *,
    radius: float = 5000,
    altitude: float,
    topodir: str = DEFAULT_TOPO_DIR,
) -> float:
    """Returns the relative height for a lat/lon/altitude height.

    :param lat: Latitude
    :param lon: Longitude
    :param altitude: Altitude (meters)
    :param radius: Radius (meters), defaults to 5000
    :return: Relative height.

    Note:
    -----
    Relative height is the height relative to the lowest point within a given radius.
    """
    topo_file = _get_topo_file_for_coord(lat, lon, topodir=topodir)

    return _get_relative_altitude(
        lat,
        lon,
        radius=radius,
        altitude=altitude,
        topography_file=topo_file,
    )
