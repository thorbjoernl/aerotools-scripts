from utils.relalt import get_relative_altitude
import sqlite3
import pathlib

EBAS_FILE_INDEX = pathlib.Path(
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/ebas_file_index.sqlite3"
)


con = sqlite3.connect(EBAS_FILE_INDEX)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute(
    """
    SELECT station_code, station_name, station_latitude, station_longitude, station_altitude FROM station
    """
)

stations = [dict(x) for x in cur.fetchall()]

mountain_sites = []
for s in stations:
    if s["station_altitude"] is None:
        print(f"No altitude for station '{s['station_code']}'")
        continue
    
    try:
        ralt = get_relative_altitude(float(s["station_latitude"]), float(s["station_longitude"]), radius = 5000, altitude = float(s["station_altitude"]), topodir = "./topo/nc")
    except ValueError:
        print(f"Station location does not fall within bounds of topo files")
        continue

    print(f"{s['station_code']} - {ralt:.2f}")
    if ralt >= 1000:
        mountain_sites.append(s["station_code"])

with open("mountain_sites.txt", "w") as f:
    f.write("\n".join(mountain_sites))
