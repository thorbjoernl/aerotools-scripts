import logging
import pprint
import datetime
from utils import fetch_json

logger = logging.getLogger(__name__)

PROJECT = "rv5_series"
EXPERIMENT = "DSemep"

# True: Use aeroval-test API. False: Use aeroval API.
USE_AEROVAL_TEST = True

# User namespace on aeroval-test
DATAPATH = "davids"  # Data Path value used only for aeroval-test.


class FetchHelper:
    def __init__(self, project: str, experiment: str):
        self._project = project
        self._experiment = experiment

    def get_ts(
        self,
        varname: str,
        region: str,
        model: str,
        obsnetwork: str,
        layer: str,
        frequency: str,
    ) -> dict:
        """
        Returns ts plot data as shown on Aeroval for the provided arguments.
        """
        scatter = fetch_json(
            f"/ts/{self._project}/{self._experiment}/{region}/{obsnetwork}/{varname}/{layer}",
            aeroval_test=USE_AEROVAL_TEST,
            user_name_space=DATAPATH,
        )

        new = {
            # Timestamps are in milliseconds since 1970-01-01
            "date": [
                datetime.datetime.fromtimestamp(x / 1000)
                for x in scatter[model][f"{frequency}_date"]
            ],
            "obs": scatter[model][f"{frequency}_obs"],
            "mod": scatter[model][f"{frequency}_mod"],
        }

        # Keep additional metadata about the time series.
        for k in (
            "station_name",
            "pyaerocom_version",
            "obs_var",
            "mod_var",
            "obs_unit",
            "mod_unit",
            "obs_name",
            "model_name",
        ):
            new[k] = scatter[model][k]

        return new

    def get_map_data(
        self,
        varname: str,
        obsnetwork: str,
        model: str,
        layer: str,
        period: str,
        season: str,
        statistics: str,
    ) -> dict:
        """
        Fetches the statistics map data that would displayed on the map on Aeroval for the given arguments.
        The returned dictionary includes the following keys:
        - station_name
        - latitude
        - longitude
        - altitude
        - region
        - statistics - The subset of statistics values that matches period,season,statisics constraints.
        """
        map_data = fetch_json(
            f"/map/{self._project}/{self._experiment}/{obsnetwork}/{varname}/{layer}/{model}/{varname}/{period}",
            aeroval_test=USE_AEROVAL_TEST,
            user_name_space=DATAPATH,
        )

        result = []
        for station in map_data:
            new = {}
            if not statistics in station:
                continue
            if not f"{period}-{season}" in station[statistics]:
                continue

            new["station_name"] = station["station_name"]
            new["latitude"] = station["latitude"]
            new["longtitude"] = station["longitude"]
            new["altitude"] = station["altitude"]
            new["region"] = station["region"]
            new["statistics"] = station[statistics][f"{period}-{season}"]

            result.append(new)

        return result

    def get_scatter(
        self,
        frequency: str,
        varname: str,
        obsnetwork: str,
        layer: str,
        model: str,
        region: str,
        period: str,
        season: str,
    ):
        """
        Returns details about the scatterplot for the parameter combination provided. Information on the scatterplot consists
        of the correlation statistics and the timeseries data which is returned as a dict of the form {"stats": ..., "ts": ...}
        """
        scat = fetch_json(
            f"/regional_statistics/{self._project}/{self._experiment}/{frequency}/{varname}/{obsnetwork}/{layer}",
            aeroval_test=USE_AEROVAL_TEST,
            user_name_space=DATAPATH,
        )

        return {
            "stats": scat[model][varname][region][f"{period}-{season}"],
            "ts": self.get_ts(varname, region, model, obsnetwork, layer, frequency),
        }


if __name__ == "__main__":
    # Instantiate class for fetching scatter and ts data for a project/experiment.
    fetch = FetchHelper(PROJECT, EXPERIMENT)

    map_data = fetch.get_map_data(
        "concNno", "EBAS-m", "v5.3", "Surface", "2022", "DJF", "yearly"
    )

    pprint.pprint(map_data[0])

    for x in [x["station_name"] for x in map_data]:
        print(x)

    scatter = fetch.get_scatter(
        "yearly", "concNno", "EBAS-m", "Surface", "v5.3", "ALL", "2022", "all"
    )

    pprint.pprint(scatter)

# > python 02-map-scatter.py
# {'altitude': 110.0,
#  'latitude': 38.366667,
#  'longtitude': 23.083333,
#  'region': ['Greece'],
#  'station_name': 'Aliartos',
#  'statistics': {'R': None,
#                 'R_kendall': None,
#                 'R_spatial_mean': None,
#                 'R_spatial_median': None,
#                 'R_spearman': None,
#                 'R_temporal_mean': None,
#                 'R_temporal_median': None,
#                 'data_mean': None,
#                 'data_std': None,
#                 'fge': None,
#                 'mab': None,
#                 'mb': None,
#                 'mnmb': None,
#                 'nmb': None,
#                 'num_valid': None,
#                 'refdata_mean': None,
#                 'refdata_std': None,
#                 'rms': None,
#                 'totnum': None,
#                 'weighted': None}}
# Aliartos
# Anholt
# Aston Hill
# Barcarrota
# Birmingham Air Quality Site (BAQS)
# Bush
# Cabauw Wielsekade
# Cabo de Creus
# Charlton Mackrell
# Chilbolton Observatory
# De Zilk
# Diabla Gora
# Doñana
# Eibergen
# Els Torms
# High Muffles
# Houtem
# Hyytiälä
# Ispra
# Keldsnor
# Kollumerwaard
# Ladybower Res.
# Lullington Heath
# Mahón
# Moerkerke
# Narberth
# Neuglobsow
# Niembro
# Oulanka
# Payerne
# Risø
# SIRTA Atmospheric Research Observatory
# St. Osyth
# Ulborg
# Utö
# Virolahti III
# Vredepeel
# Waldhof
# Wicken Fen
# Yarner Wood
# Zingst
# {'stats': {'R': 0.668341,
#            'R_kendall': 0.680488,
#            'R_spatial_mean': 0.668341,
#            'R_spearman': 0.828397,
#            'R_temporal_median': None,
#            'data_mean': 0.366163,
#            'data_std': 0.459987,
#            'fge': 0.491691,
#            'mab': 0.192625,
#            'mb': -0.062496,
#            'mnmb': -0.340959,
#            'nmb': -0.145794,
#            'num_coords_tot': 46.0,
#            'num_coords_with_data': 41.0,
#            'num_valid': 41.0,
#            'refdata_mean': 0.428659,
#            'refdata_std': 0.418093,
#            'rms': 0.365004,
#            'totnum': 46.0,
#            'weighted': 0.0},
#  'ts': {'date': [1656633600000],
#         'mod': [0.36616],
#         'mod_unit': 'ug N m-3',
#         'mod_var': 'concNno',
#         'model_name': 'v5.3',
#         'obs': [0.42866],
#         'obs_name': 'EBAS-m',
#         'obs_unit': 'ug N m-3',
#         'obs_var': 'concNno',
#         'pyaerocom_version': '0.21.0',
#         'station_name': 'ALL'}}
