import requests
import simplejson
import sqlite3
import logging

logger = logging.getLogger(__name__)

PROJECT = "rv5_series"
EXPERIMENT = "DSemep"


# True: Use aeroval-test API. False: Use aeroval API.
USE_AEROVAL_TEST = True

# User namespace on aeroval-test
DATAPATH = "davids"  # Data Path value used only for aeroval-test.

HTTP_OK = 200

EBAS_FILE_INDEX_PATH = "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/ebas_file_index.sqlite3"


def build_station_code_lookup_table() -> dict[str, str]:
    """Aeroval currently does not include station code (and other metadata) as part of
    the data provided, so this reads the station names and IDs from the EBAS file index
    and attempts to create a lookup table that maps a station name to its metadata.

    The following metadata is included as of writing this documentation:
        station_code
        platform_code
        station_name
        station_wdca_id
        station_gaw_name
        station_gaw_id
        station_airs_id
        station_other_ids
        station_state_code
        station_landuse
        station_setting
        station_gaw_type
        station_wmo_region
        station_latitude
        station_longitude
        station_altitude
    """
    con = sqlite3.connect(EBAS_FILE_INDEX_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute(
        """
        SELECT * FROM station         
        """
    )
    rows = cur.fetchall()
    lookup = {}
    for row in rows:
        name = row["station_name"]
        if name in rows:
            raise Exception(
                "Duplicate station name. Reverse lookup of station name not possible."
            )

        lookup[name] = {k: v for k, v in dict(row).items()}

    return lookup


station_code_lookup_table = build_station_code_lookup_table()


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


time_config = {
    "year": "2022",
    "season": "DJF",
    "stats": "daily",
}


def get_site_data(
    varname: str, obsnetwork: str, model: str, layer: str, time_config: dict
) -> dict[str, dict]:
    """
    :param varname : Observation and model variable name (eg. concNno)
    :param obsnetwork : Observation network (eg. EBAS-m)
    :param model : Model name (eg. v5.3)
    :param layer : Layer (eg. Surface)
    :param time_config : Dict with entries 'year', 'season', 'stats' (see example above)
    """
    year = time_config["year"]
    season = time_config["season"]
    stats = time_config["stats"]

    map_data = fetch_json(
        f"/map/{PROJECT}/{EXPERIMENT}/{obsnetwork}/{varname}/{layer}/{model}/{varname}/{year}"
    )
    result = {}
    for md in map_data:
        station_name = md["station_name"]
        extracted_data = station_code_lookup_table[station_name]

        station_code = extracted_data["station_code"]

        # Skip stations for which stats timeseries or year/season combination does
        # not exist by not appending them to results array. This should result in
        # the same list of stations as aeroval shows with the above options.
        if not stats in md:
            continue
        if not f"{year}-{season}" in md[stats]:
            continue
        extracted_data = station_code_lookup_table[station_name]

        # Aeroval API returns lat, lon. Compare and warn if they differ as an
        # additional sanity check to catch mistakes.
        if not md["latitude"] == extracted_data["station_latitude"]:
            logger.warning(
                f"Ebas index latitude ({md['latitude']:.5f}) does not match api provided latitude ({extracted_data['station_latitude']:.5f})."
            )
        if not md["longitude"] == extracted_data["station_longitude"]:
            logger.warning(
                f"Ebas index longitude ({md['longitude']:.5f}) does not match api provided longitude ({extracted_data['longitude']:.5f})."
            )

        # Append result
        result[station_code] = extracted_data

    return result


sites = get_site_data("concNno", "EBAS-m", "v5.3", "Surface", time_config)

# Show full record for the first entry:
print(sites["GR0001R"])

# List names for all entries:
for station_code in sites:
    print(f"{station_code} - {sites[station_code]['station_name']}")

print(len(sites))
# OUTPUT:
# python main.py
# {'station_code': 'GR0001R', 'platform_code': 'GR0001S', 'station_name': 'Aliartos', 'station_wdca_id': None, 'station_gaw_name': None, 'station_gaw_id': None, 'station_airs_id': None, 'station_other_ids': None, 'station_state_code': None, 'station_landuse': None, 'station_setting': None, 'station_gaw_type': None, 'station_wmo_region': None, 'station_latitude': 38.366667, 'station_longitude': 23.083333, 'station_altitude': 110.0}
# GR0001R - Aliartos
# DK0008R - Anholt
# GB0031R - Aston Hill
# ES0011R - Barcarrota
# GB0101U - Birmingham Air Quality Site (BAQS)
# GB0033R - Bush
# NL0644R - Cabauw Wielsekade
# ES0010R - Cabo de Creus
# GB0053R - Charlton Mackrell
# GB1055R - Chilbolton Observatory
# NL0091R - De Zilk
# PL0005R - Diabla Gora
# ES0017R - Doñana
# NL0007R - Eibergen
# ES0014R - Els Torms
# GB0014R - High Muffles
# BE0013R - Houtem
# FI0050R - Hyytiälä
# IT0004R - Ispra
# DK0005R - Keldsnor
# NL0009R - Kollumerwaard
# GB0037R - Ladybower Res.
# GB0038R - Lullington Heath
# ES0006R - Mahón
# BE0011R - Moerkerke
# GB0043R - Narberth
# DE0007R - Neuglobsow
# ES0008R - Niembro
# FI0022R - Oulanka
# CH0002R - Payerne
# DK0012R - Risø
# FR0020R - SIRTA Atmospheric Research Observatory
# GB0050R - St. Osyth
# DK0031R - Ulborg
# FI0009R - Utö
# FI0018R - Virolahti III
# NL0010R - Vredepeel
# DE0002R - Waldhof
# GB0045R - Wicken Fen
# GB0013R - Yarner Wood
# DE0009R - Zingst
# 41
