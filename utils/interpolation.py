import numpy as np
import xarray as xr

# https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html#latitude-coordinate
# https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html#longitude-coordinate
UNITS_LAT = set(["degrees_north", "degree_north", "degree_N", "degrees_N", "degreeN", "degreesN"])
UNITS_LON = set(["degrees_east", "degree_east", "degree_E", "degrees_E", "degreeE", "degreesE"])


def _find_lat_lon_var_names(data: xr.Dataset) -> tuple[str, str]:
    for var_name in data.coords:
        unit_str = data[var_name].attrs.get("units", None)
        if unit_str in UNITS_LAT:
            lat_var = var_name
            continue
        if unit_str in UNITS_LON:
            lon_var = var_name

    assert not any([x is None for x in [lat_var, lon_var]])

    return lat_var, lon_var

def get_bilinear_interpolation(data: xr.Dataset, lat: np.ndarray, lon: np.ndarray) -> xr.Dataset:
    lat_var, lon_var = _find_lat_lon_var_names(data)

    # https://docs.xarray.dev/en/latest/user-guide/interpolation.html
    interpolated = data.interp(
        {
            lat_var: lat,
            lon_var: lon,
        },
        method="linear"
    )

    return interpolated


