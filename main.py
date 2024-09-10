import requests
import simplejson

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

    print(f"Fetching data from '{url}'")
    r = requests.get(url)
    if r.status_code == HTTP_OK:
        return simplejson.loads(r.content)
    else:
        print(f"Fetching data from '{url}' failed with status code {r.status_code}")
        return None


time_config = {
    "year": "2022",
    "season": "DJF",
    "stats": "daily",
}


def get_site_data(varname: str, obsnetwork: str, model: str, time_config: dict) -> dict:
    """

    :param varname : Observation and model variable name (eg. concNno)
    :param obsnetwork : Observation network (eg. EBAS-m)
    :param model : Model name (eg. v5.3)
    :param time_config : Dict with entries 'year', 'season', 'stats' (see example above)
    """
    layer = "Surface"  # TODO: Hardcoded for now.
    year = time_config["year"]
    season = time_config["season"]
    stats = time_config["stats"]

    map_data = fetch_json(
        f"/map/{PROJECT}/{EXPERIMENT}/{obsnetwork}/{varname}/{layer}/{model}/{varname}/{year}"
    )
    result = []
    for md in map_data:
        # Loop through station entries extracting their characteristics.
        extracted_data = {
            k: v
            for k, v in md.items()
            if k in ["station_name", "latitude", "longitude", "altitude", "region"]
        }

        # Skip stations for which stats timeseries or year/season combination does
        # not exist by not appending them to results array.
        if not stats in md:
            continue
        if not f"{year}-{season}" in md[stats]:
            continue

        # Append result
        result.append(extracted_data)

    return result


sites = get_site_data("concNno", "EBAS-m", "v5.3", time_config)

# Show full record for the first entry:
print(sites[0])

# List names for all entries:
for name in [s["station_name"] for s in sites]:
    print(name)

# OUTPUT:
# python main.py 
# Fetching data from 'https://api.aeroval-test.met.no/api/0.2.1/map/rv5_series/DSemep/EBAS-m/concNno/Surface/v5.3/concNno/2022?data_path=davids'
# {'station_name': 'Aliartos', 'latitude': 38.366667, 'longitude': 23.083333, 'altitude': 110.0, 'region': ['Greece']}
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