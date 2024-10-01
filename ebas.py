import datetime
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

EBAS_FILE_INDEX = pathlib.Path(
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/ebas_file_index.sqlite3"
)
FOLDER_TO_READ = pathlib.Path(
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data"
)


def ebas_components_for_aerocom_variable(aerocom_variable: str):
    return EbasVarInfo(aerocom_variable)["component"]


def get_datasets(
    var_name: str,
    sites: list[str] | str,
    matrix: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
):
    if isinstance(sites, str):
        sites = [sites]
    con = sqlite3.connect(str(EBAS_FILE_INDEX))
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    comps = ebas_components_for_aerocom_variable(var_name)

    cur.execute(
        f"""
        SELECT DISTINCT filename,station_code,comp_name,unit,matrix
        
        FROM 
            variable
        WHERE
            station_code IN ({",".join('?'*len(sites))})
            AND comp_name IN ({",".join('?'*len(comps))}) 
            AND matrix = ?
            AND first_start >= ?
            AND last_end <= ?
        GROUP BY
            filename
        """,
        (*sites, *comps, matrix, start_time, end_time),
    )
    return cur.fetchall()


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
    with engines["nilupmfebas"].open(
        file_name,
        filters=[pyaro.timeseries.filters.get("stations", include=tuple(SITES))],
    ) as ts:

        ebas_var = None
        for x in ebas_components_for_aerocom_variable(VAR_NAME):
            for y in ts.variables():
                if f"{MATRIX}#{x}#" in y:
                    print(f"Using variable name '{y}'")
                    ebas_var = y

                    data: pyaro.timeseries.NpStructuredData = ts.data(ebas_var)
                    if df is None:
                        df = pd.DataFrame(
                            {
                                "start_time": data.start_times,
                                "end_time": data.end_times,
                                "latitude": data.latitudes,
                                "longitude": data.longitudes,
                                "altitude": data.altitudes,
                                "station": data.stations,
                                "flag": data.flags,
                                f"value_{ebas_var}": data.values,
                                f"stdev_{ebas_var}": data.standard_deviations,
                            }
                        )
                    else:
                        df[f"value_{ebas_var}"] = data.values
                        df[f"stdev_{ebas_var}"] = data.standard_deviations

    return df


if __name__ == "__main__":
    VAR_NAME = "concso4"
    SITES = ["AT0002R", "NO0001R"]
    MATRIX = "aerosol"
    START_TIME = datetime.datetime(2010, 1, 1, 0, 0, 0)
    END_TIME = datetime.datetime(2011, 12, 31, 23, 59, 59)

    files = get_datasets(VAR_NAME, SITES, MATRIX, START_TIME, END_TIME)

    print(f"{len(files)} files found")

    # Example access of data for a file
    data = {}
    for f in [f"{FOLDER_TO_READ}/{x['filename']}" for x in files]:
        print(f"Reading file '{f}'...")
        data[f] = read_ebas_data(f)

    # data is now a dictionary mapping from the source file_path to the corresponding loaded data
    # frame.
    print(list(data.values())[0])
    print(list(data.values())[0].columns)
