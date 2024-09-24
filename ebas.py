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
    # 206 files found
    # ...
    #     - AT0002R.20080101080000.20110303000000.wet_only_sampler..precip.1y.1d.AT01L_wados_02..lev2.nas
    #   - sulphate_corrected (mg S/l)
    #   - sulphate_corrected (mg/l)
    #   - sulphate_total (mg S/l)
    #   - sulphate_total (mg/l)
    # - AT0002R.20090101080000.20110303000000.wet_only_sampler..precip.1y.1d.AT01L_wados_02..lev2.nas
    #   - sulphate_corrected (mg S/l)
    #   - sulphate_corrected (mg/l)
    #   - sulphate_total (mg S/l)
    #   - sulphate_total (mg/l)
    # - AT0002R.20090101080000.20110303000000.wet_only_sampler..precip.1y.1d.AT01L_wados_02..lev2.nas
    #   - sulphate_corrected (mg S/l)
    #   - sulphate_corrected (mg/l)
    #   - sulphate_total (mg S/l)
    #   - sulphate_total (mg/l)
    # - AT0002R.20100101000000.20140227000000.filter_3pack..aerosol.1y.1d.AT01L_f3p_02..lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    # - AT0002R.20100101000000.20140227000000.filter_3pack..aerosol.1y.1d.AT01L_f3p_02..lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    # - AT0002R.20110101000000.20140227000000.filter_3pack..aerosol.6d.1d.AT01L_f3p_02..lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    # - AT0002R.20110101000000.20140227000000.filter_3pack..aerosol.6d.1d.AT01L_f3p_02..lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    # - AT0002R.20220712000000.20240530000000.high_vol_sampler..pm25.10d.1d.AT03L_hvs_at0002.FR18L_tracers_IMP2022.lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    # - AT0002R.20220712000000.20240530000000.high_vol_sampler..pm25.10d.1d.AT03L_hvs_at0002.FR18L_tracers_IMP2022.lev2.nas
    #   - sulphate_total (ug S/m3)
    #   - sulphate_total (ug/m3)
    #Using variable name 'precip#sulphate_corrected#mg S/l'
    #Using variable name 'precip#sulphate_corrected#mg/l'
    #Using variable name 'precip#sulphate_total#mg S/l'
    #Using variable name 'precip#sulphate_total#mg/l'
    #Column names: Index(['start_time', 'end_time', 'latitude', 'longitude', 'altitude',
    #       'station', 'flag', 'value_precip#sulphate_corrected#mg S/l',
    #       'stdev_precip#sulphate_corrected#mg S/l',
    #       'value_precip#sulphate_corrected#mg/l',
    #       'stdev_precip#sulphate_corrected#mg/l',
    #       'value_precip#sulphate_total#mg S/l',
    #       'stdev_precip#sulphate_total#mg S/l',
    #       'value_precip#sulphate_total#mg/l', 'stdev_precip#sulphate_total#mg/l'],
    #      dtype='object')
    #             start_time            end_time  ...  value_precip#sulphate_total#mg/l  stdev_precip#sulphate_total#mg/l
    #0   1987-01-01 07:00:00 1987-01-02 07:00:00  ...                               1.9                               NaN
    #1   1987-01-02 07:00:00 1987-01-03 07:00:00  ...                               NaN                               NaN
    #2   1987-01-03 07:00:00 1987-01-04 07:00:00  ...                               NaN                               NaN
    #3   1987-01-04 07:00:00 1987-01-05 07:00:00  ...                               NaN                               NaN
    #4   1987-01-05 07:00:00 1987-01-06 07:00:00  ...                               NaN                               NaN
    #..                  ...                 ...  ...                               ...                               ...
    #360 1987-12-27 07:00:00 1987-12-28 07:00:00  ...                               NaN                               NaN
    #361 1987-12-28 07:00:00 1987-12-29 07:00:00  ...                               4.2                               NaN
    #362 1987-12-29 07:00:00 1987-12-30 07:00:00  ...                               NaN                               NaN
    #363 1987-12-30 07:00:00 1987-12-31 07:00:00  ...                               NaN                               NaN
    #364 1987-12-31 07:00:00 1988-01-01 07:00:00  ...                               NaN                               NaN
    #
    #[365 rows x 15 columns]