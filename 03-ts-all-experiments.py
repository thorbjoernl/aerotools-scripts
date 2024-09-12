import json
import pprint
import requests
import logging


logger = logging.getLogger()

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

def get_station_names(project: str, experiment: str, obs_network: str, varname: str, layer: str, model: str, period: str) -> list:
    """
    Fetches the available station names for the parameters provided.
    """
    data = fetch_json(f"/map/{project}/{experiment}/{obs_network}/{varname}/{layer}/{model}/{varname}/{period}")
    if data is None:
        return []
    
    return [x["station_name"] for x in data]

def get_ts(varname: str, region: str, model: str, obsnetwork: str, layer: str, period: str, season: str, frequency: str) -> dict:
    """
    Returns ts plot data as shown on Aeroval for the provided arguments.
    """
    scatter = fetch_json(f"/ts/{PROJECT}/{EXPERIMENT}/{region}/{obsnetwork}/{varname}/{layer}")

    new = {
        "date": scatter[model][f"{frequency}_date"],
        "obs": scatter[model][f"{frequency}_obs"],
        "mod": scatter[model][f"{frequency}_mod"],
    }

    # Keep additional metadata about the time series.
    for k in ("station_name", "pyaerocom_version", "obs_var", "mod_var", "obs_unit", "mod_unit", "obs_name", "model_name"):
        new[k] = scatter[model][k]

    return new

LAYER = "Surface"
VARNAME = "concNno"
PERIOD = "2022"
MODEL = "v5.3"
OBSNETWORK = "EBAS-m"
SEASON = "all"
FREQUENCY = "monthly"

ts_data = {}
for exp in get_experiments(PROJECT):
    available_stations = get_station_names(PROJECT, exp, OBSNETWORK, VARNAME, LAYER, MODEL, PERIOD)
    if available_stations:
        ts_data[exp] = {}
    print(available_stations) 
    for station in available_stations:
        ts_data[exp][station] = get_ts(VARNAME, station, MODEL, OBSNETWORK, LAYER, PERIOD, SEASON, FREQUENCY)
        

#pprint.pprint(ts_data)

pprint.pprint(ts_data["DSemep"])