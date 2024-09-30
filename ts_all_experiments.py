import json
import pprint
import requests
import logging


logger = logging.getLogger(__name__)

PROJECT = "rv5_series"
EXPERIMENT = "DSemep"

# True: Use aeroval-test API. False: Use aeroval API.
USE_AEROVAL_TEST = True

# User namespace on aeroval-test
DATAPATH = "davids"  # Data Path value used only for aeroval-test.

HTTP_OK = 200


def fetch_json(path: str) -> dict:
    """
    Helper function to fetch and parse json from some path on api.aeroval[-test].met.no.
    """
    if USE_AEROVAL_TEST:
        url = f"https://api.aeroval-test.met.no/api/0.2.1{path}?data_path={DATAPATH}"
    else:
        url = f"https://api.aeroval.met.no/api/0.2.1{path}"

    logger.info(f"Fetching data from '{url}'")
    r = requests.get(url)
    if r.status_code == HTTP_OK:
        return json.loads(r.content)
    else:
        logger.error(
            f"Fetching data from '{url}' failed with status code {r.status_code}"
        )
        return None


def get_experiments(project: str) -> list[str]:
    """
    Lists the public experiments for the project.
    """
    experiments = fetch_json(f"/experiments/{project}")

    return [e for e in experiments if experiments[e]["public"]]


def get_station_names(
    project: str,
    experiment: str,
    obs_network: str,
    varname: str,
    layer: str,
    model: str,
    period: str,
) -> list:
    """
    Fetches the available station names for the parameters provided.
    """
    data = fetch_json(
        f"/map/{project}/{experiment}/{obs_network}/{varname}/{layer}/{model}/{varname}/{period}"
    )
    if data is None:
        return []

    return [x["station_name"] for x in data]


def get_ts(
    varname: str,
    region: str,
    model: str,
    obsnetwork: str,
    layer: str,
    period: str,
    season: str,
    frequency: str,
) -> dict:
    """
    Returns ts plot data as shown on Aeroval for the provided arguments.
    """
    scatter = fetch_json(
        f"/ts/{PROJECT}/{EXPERIMENT}/{region}/{obsnetwork}/{varname}/{layer}"
    )

    new = {
        "date": scatter[model][f"{frequency}_date"],
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

if __name__ == "__main__":
    LAYER = "Surface"
    VARNAME = "concNno"
    PERIOD = "2022"
    MODEL = "v5.3"
    OBSNETWORK = "EBAS-m"
    SEASON = "all"
    FREQUENCY = "monthly"

    ts_data = {}
    for exp in get_experiments(PROJECT):
        available_stations = get_station_names(
            PROJECT, exp, OBSNETWORK, VARNAME, LAYER, MODEL, PERIOD
        )
        # "ALL" is treated as a special case 'station' but isn't found using the above function
        # append it to include it.
        available_stations.append("ALL")
        if available_stations:
            ts_data[exp] = {}
        for station in available_stations:
            ts_data[exp][station] = get_ts(
                VARNAME, station, MODEL, OBSNETWORK, LAYER, PERIOD, SEASON, FREQUENCY
            )


    pprint.pprint(ts_data["DSemep"]["Ulborg"])

    pprint.pprint(ts_data["DSemep"]["ALL"])

# > python 03-ts-all-experiments.py
# ...
# {'date': [1642204800000,
#          1644883200000,
#          1647302400000,
#          1649980800000,
#          1652572800000,
#          1655251200000,
#          1657843200000,
#          1660521600000,
#          1663200000000,
#          1665792000000,
#          1668470400000,
#          1671062400000],
# 'mod': [0.01544,
#         0.02262,
#         0.11107,
#         0.09903,
#         0.06891,
#         0.06558,
#         0.12066,
#         None,
#         None,
#         0.06131,
#         0.03328,
#         0.03677],
# 'mod_unit': 'ug N m-3',
# 'mod_var': 'concNno',
# 'model_name': 'v5.3',
# 'obs': [-0.02536,
#         -0.1396,
#         0.18742,
#         0.19061,
#         0.11795,
#         0.07586,
#         0.13181,
#         None,
#         None,
#         0.05669,
#         -0.1508,
#         0.19174],
# 'obs_name': 'EBAS-m',
# 'obs_unit': 'ug N m-3',
# 'obs_var': 'concNno',
# 'pyaerocom_version': '0.21.0',
# 'station_name': 'Ulborg'}
