import pyaro
import pandas as pd
import pyaro.timeseries
import pathlib
import logging
import sqlite3
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom import const

logger = logging.getLogger(__name__)

vars = const.VARS

EBAS_FILE_INDEX = pathlib.Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/ebas_file_index.sqlite3")
FOLDER_TO_READ = pathlib.Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data")


def ebas_components_for_aerocom_variable(aerocom_variable: str):
    return EbasVarInfo(aerocom_variable)["component"]

#print(ebas_components_for_aerocom_variable("conco3"))
VAR_NAME = 'concso4'
SITE = 'AT0002R'

con = sqlite3.connect(str(EBAS_FILE_INDEX))
cur = con.cursor()

all = []

for comp in ebas_components_for_aerocom_variable(VAR_NAME):
    cur.execute(
        """
        SELECT station_code,comp_name,unit, filename FROM variable
        WHERE
            station_code = ? AND comp_name = ?
        """,
        (SITE, comp)
    )
    all.extend(cur.fetchall())

def read_ebas_data(file_name: str) -> pd.DataFrame:
    """
    Reads data from a single ebas .nas file providing it as a pandas data frame.
    The resulting column will contain data for separate components as two colums
    (one for the values and one for the standard deviations named 'value_{ebas_var}'
    and 'stdev_{ebas_var}'). ebas_var is the component name used by pyaro which is
    '{matrix}#{comp_name}#{unit}' (eg. 'precip#precipitation_amount#mm').
    """
    engines = pyaro.list_timeseries_engines()
    df = None
    with engines["nilupmfebas"].open(file_name,
        filters=[pyaro.timeseries.filters.get("stations", include=[SITE])]) as ts:

        ebas_var = None
        for x in ebas_components_for_aerocom_variable(VAR_NAME):
            for y in ts.variables():
                if f"#{x}#" in y:
                    print(f"Using variable name '{y}'")
                    ebas_var = y

                    data: pyaro.timeseries.NpStructuredData = ts.data(ebas_var)
                    if df is None:
                        df = pd.DataFrame({
                            "start_time": data.start_times,
                            "end_time": data.end_times,
                            "latitude": data.latitudes,
                            "longitude": data.longitudes,
                            "altitude": data.altitudes,
                            "station": data.stations,
                            "flag": data.flags,
                            f"value_{ebas_var}": data.values,
                            f"stdev_{ebas_var}": data.standard_deviations,
                        })
                    else:
                        df[f"value_{ebas_var}"] = data.values
                        df[f"stdev_{ebas_var}"] = data.standard_deviations

    return df 

def get_component_info(file_names: list[str], aerocom_var: str | None = None):
    """
    Returns a dictionary of information about components provided by
    ebas files. The dictionary has a single entry per file path with a sub dict
    containing a list of pairwise comp_names and units.

    If aerocom_var is set, only components that apply to that aerocom variable
    name will be listed.

    """
    con = sqlite3.connect(str(EBAS_FILE_INDEX))
    cur = con.cursor()

    files = set(file_names)
    result = {}
    cur.execute(
        """
        SELECT comp_name,unit,filename FROM variable
        """
    )

    for x in cur.fetchall():
        if x[2] in files:
            if x[2] not in result:
                result[x[2]] = {}
            if "component" not in result[x[2]]:
                result[x[2]]["component"] = []
            if "unit" not in result[x[2]]:
                result[x[2]]["unit"] = []

            if x[0] in ebas_components_for_aerocom_variable(aerocom_var) or aerocom_var is None:
                result[x[2]]["component"].append(x[0])
                result[x[2]]["unit"].append(x[1])

    return result

if __name__ == "__main__":
    print (f"{len(all)} files found")

    # Print available files and components for the selected station
    # and aerocom variable name.
    info = get_component_info([x[3] for x in all], VAR_NAME)
    for f in all:
        print (f" - {f[3]}")
        for c, u in zip(info[f[3]]["component"], info[f[3]]["unit"]):
            print (f"   - {c} ({u})")

    # Example access of data for a file
    data = read_ebas_data(f"{FOLDER_TO_READ}/AT0002R.19870101070000.20110303000000.wet_only_sampler..precip.1y.1d.AT01L_wados_02.AT01L_IC_a.lev2.nas")
    print(f"Column names: {data.columns}")
    print(data)

    # Example output:
