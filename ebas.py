import pyaerocom
import os
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
import pandas as pd


EBAS_DATA_DIR = (
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data"
)
VARIABLE = "conco3"
SITE = "St. Osyth"

ebas_variable = EbasVarInfo(VARIABLE)["component"][0]

file_index = pyaerocom.io.EbasFileIndex(f"{EBAS_DATA_DIR}/ebas_file_index.sqlite3")

print(ebas_variable)
file_index = pyaerocom.io.EbasFileIndex(f"{EBAS_DATA_DIR}/ebas_file_index.sqlite3")

print(pyaerocom.io.EbasSQLRequest(variables=ebas_variable, station_names=SITE))

# It takes quite some time to query for the list of files in Ebas, so caching the returned list of files.
# cache.txt must be deleted when changing site and/or variable.
if os.path.exists("cache.txt"):
    with open("cache.txt", "r") as f:
        files = [x.strip() for x in f.readlines()]
else:
    files = file_index.get_file_names(
        pyaerocom.io.EbasSQLRequest(variables=ebas_variable, station_names=SITE)
    )

    with open("cache.txt", "w") as f:
        f.writelines([f"{x}\n" for x in files])

df = None
for fp in files:
    print(fp)
    ebas = EbasNasaAmesFile(f"{EBAS_DATA_DIR}/data/{fp}")
    print(ebas.col_names)
    timestamps = ebas.compute_time_stamps()

    dt = {
        "start_time": timestamps[0],
        "end_time": timestamps[1],
        f"{ebas_variable}_1": ebas.data[:, 2],
        f"{ebas_variable}_2": ebas.data[:, 3],
        "numflag": ebas.data[:, 4],
    }

    if df is None:
        df = pd.DataFrame(dt)
    else:
        df = pd.concat([df, pd.DataFrame(dt)])

df = df.sort_values("start_time")


print(df[:100])

# with pyaro.list_timeseries_engines()["nilupmfebas"].open(f"{EBAS_DATA_DIR}/data",
#        filters=[pyaro.timeseries.filters.get("stations", include=[SITE]),
#                 pyaro.timeseries.filters.get("variables", include=[ebas_variable])]
#                 ) as ts:
#    print(ts.variables())
