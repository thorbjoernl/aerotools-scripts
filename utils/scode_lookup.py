import sqlite3


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
        name = row["station_name"].strip()
        if name in rows:
            raise Exception(
                "Duplicate station name. Reverse lookup of station name not possible."
            )

        lookup[name] = {k: v for k, v in dict(row).items()}

    return lookup


station_code_lookup_table = build_station_code_lookup_table()