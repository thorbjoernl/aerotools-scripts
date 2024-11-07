import xarray as xr
import numpy as np
from .const import EARTH_RADIUS, DEFAULT_TOPO_DIR
import json
import os
import logging
from functools import cache


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
    lat: float, lon: float, *, radius: float = 5000, altitude: float, fun: str = "min", topography_file
):
    topo = _load_topo(topography_file)

    # At most one degree of latitude (at equator) is roughly 111km.
    # Subsetting to based on this value with safety margin makes the
    # distance calculation MUCH more efficient.

    s = 0.1 + (radius/1000)/100
    topo = topo.sel(lon=slice(lon-s, lon+s), lat=slice(lat-s, lat+s))
    topo = topo.fillna(0)

    distances = _haversine(topo["lon"], topo["lat"], lon, lat)

    within_radius = distances <= radius

    values_within_radius = topo["Band1"].where(within_radius, other=False, drop=True)

    fun = getattr(values_within_radius, fun)
    min_value = float(fun())
    return altitude - max([min_value, 0])

@cache
def _load_topo(a_file):
    return xr.open_dataset(a_file)

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
    fun: str = "min",
    topodir: str = DEFAULT_TOPO_DIR,
) -> float:
    """Returns the relative height for a lat/lon/altitude height.

    :param lat: Latitude
    :param lon: Longitude
    :param altitude: Altitude (meters)
    :param radius: Radius (meters), defaults to 5000
    :param fun: string name of a function to be used to determine the value 
        against which to calculate the relative altitude (eg. 'min', 'mean', 'median')
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
        fun = fun,
        topography_file=topo_file,
    )
