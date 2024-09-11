import requests
import simplejson
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
        return simplejson.loads(r.content)
    else:
        logger.error(
            f"Fetching data from '{url}' failed with status code {r.status_code}"
        )
        return None
    

def get_map_data(varname: str, obsnetwork: str, model: str, layer: str, period: str, season: str, statistics: str):
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
        f"/map/{PROJECT}/{EXPERIMENT}/{obsnetwork}/{varname}/{layer}/{model}/{varname}/{period}"
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

def get_scatter(varname: str, region: str, model: str, obsnetwork: str, layer: str, period: str, season: str, frequency: str):
    """
    Returns scatter plot data as shown on Aeroval for the provided arguments.
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


map_data = get_map_data("concNno", "EBAS-m", "v5.3", "Surface", "2022", "DJF", "yearly")

print(map_data[0]["statistics"])

for x in [x["station_name"] for x in map_data]:
    print(x)


print(get_scatter("concNno", "ALL", "v5.3", "EBAS-m", "Surface", "2022", "DJF", "monthly"))
