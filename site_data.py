import pprint
import logging
from utils import fetch_json, station_code_lookup_table

logger = logging.getLogger(__name__)

# Used as tolerance for comparing api provided tolerances and ebas file
# index provided tolerances. Differences above this value will cause a
# warning.
COORD_TOLERANCE = 0.0001

PROJECT = "rv5_series"
EXPERIMENT = "DSemep"


# True: Use aeroval-test API. False: Use aeroval API.
USE_AEROVAL_TEST = True

# User namespace on aeroval-test
DATAPATH = "davids"  # Data Path value used only for aeroval-test.

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
        f"/map/{PROJECT}/{EXPERIMENT}/{obsnetwork}/{varname}/{layer}/{model}/{varname}/{year}",
        aeroval_test=USE_AEROVAL_TEST,
        user_name_space=DATAPATH,
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
        if abs(md["latitude"] - extracted_data["station_latitude"]) > COORD_TOLERANCE:
            logger.warning(
                f"Ebas index latitude ({md['latitude']:.5f}) does not match api provided latitude ({extracted_data['station_latitude']:.5f})."
            )
        if abs(md["longitude"] - extracted_data["station_longitude"]) > COORD_TOLERANCE:
            logger.warning(
                f"Ebas index longitude ({md['longitude']:.5f}) does not match api provided longitude ({extracted_data['station_longitude']:.5f})."
            )

        # Append result
        result[station_code] = extracted_data

    return result


if __name__ == "__main__":
    sites = get_site_data("concNno", "EBAS-m", "v5.3", "Surface", time_config)

    # Show full record for the first entry:
    pprint.pprint(sites["GR0001R"])

    # List names for all entries:
    for station_code in sites:
        print(f"{station_code} - {sites[station_code]['station_name']}")

    sites = get_site_data("concNnh3", "EBAS-m", "v5.3", "Surface", time_config)

    pprint.pprint(sites["ES0031U"])
    print(
        f"Number of stations: {len(sites)}"
    )  # Should match count shown at https://aeroval-test.met.no/davids/pages/evaluation/?project=rv5_series&experiment=DSemep&station=ALL
# > python 01-site-data.py
# {'platform_code': 'GR0001S',
#  'station_airs_id': None,
#  'station_altitude': 110.0,
#  'station_code': 'GR0001R',
#  'station_gaw_id': None,
#  'station_gaw_name': None,
#  'station_gaw_type': None,
#  'station_landuse': None,
#  'station_latitude': 38.366667,
#  'station_longitude': 23.083333,
#  'station_name': 'Aliartos',
#  'station_other_ids': None,
#  'station_setting': None,
#  'station_state_code': None,
#  'station_wdca_id': None,
#  'station_wmo_region': None}
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
# Number of stations: 41
