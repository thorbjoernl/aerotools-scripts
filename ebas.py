import pyaro
import pandas as pd
import pyaro.timeseries
import pathlib
import re
import logging
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom import const

logger = logging.getLogger(__name__)

vars = const.VARS

FOLDER_TO_READ = pathlib.Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data")

#for v in vars:
#    try:
#        if len(EbasVarInfo(v.var_name)["component"]) > 1:
#            print(v.var_name, EbasVarInfo(v.var_name)["component"]) 
#    except Exception:
#        pass

def ebas_components_for_aerocom_variable(aerocom_variable: str):
    return EbasVarInfo(aerocom_variable)["component"]

#print(ebas_components_for_aerocom_variable("conco3"))
VAR_NAME = 'concso4'
SITE = 'AT0002R'

pattern = re.compile(f"/{SITE}\.")

if __name__ == "__main__":
    engines = pyaro.list_timeseries_engines()
    result = None
    ebas_var = None
    df = None
    # ebas_var = 'pm25#total_carbon#ug C m-3'
    files = list(FOLDER_TO_READ.iterdir())
    for i, f in enumerate(files, start=1):
        print(f"[{i}/{len(files)}] - {f}")
        if not (SITE in str(f)):
            # Using the pyaro stations filter requires reading all the data before filtering.
            # Applying this extra filter step to prevent unneccessary filter step (since files
            # include station id in their file name)
            #print(f"Skipping file '{f}' due to not including site id in filename.")
            continue

        print(f"Processing file '{f}'...")

        with engines["nilupmfebas"].open(f,
                filters=[pyaro.timeseries.filters.get("stations", include=[SITE])]) as ts:
            
            
            for x in ebas_components_for_aerocom_variable(VAR_NAME):
                for y in ts.variables():
                    if f"#{x}#" in y:
                        print(f"Using variable name '{y}'")
                        ebas_var = y

                        data: pyaro.timeseries.NpStructuredData = ts.data(ebas_var)
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
                        if df is None:
                            continue
                        
                        if result is None:
                            result = df
                            continue
                        
                        result = pd.merge(result, df, how="outer", on=["start_time", "end_time", "station", "latitude", "longitude", "altitude", "flag"], suffixes=("", f"_{i}"))

    result.to_csv("output.csv")
    print(result)
        #       start_time            end_time   latitude  longitude  altitude  station  flag      value  stdev
        #0  2017-11-30 2017-11-30 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.400000    NaN
        #1  2017-12-03 2017-12-03 23:58:59  47.766666  16.766666     117.0  AT0002R     0   4.390000    NaN
        #2  2017-12-06 2017-12-06 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.870000    NaN
        #3  2017-12-09 2017-12-09 23:58:59  47.766666  16.766666     117.0  AT0002R     0   1.450000    NaN
        #4  2017-12-12 2017-12-12 23:58:59  47.766666  16.766666     117.0  AT0002R     0   1.430000    NaN
        #5  2017-12-15 2017-12-15 23:58:59  47.766666  16.766666     117.0  AT0002R     0   6.370000    NaN
        #6  2017-12-18 2017-12-18 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.610000    NaN
        #7  2017-12-21 2017-12-21 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.830000    NaN
        #8  2017-12-24 2017-12-24 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.640000    NaN
        #9  2017-12-27 2017-12-27 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.490000    NaN
        #10 2018-01-02 2018-01-02 23:58:59  47.766666  16.766666     117.0  AT0002R     0   4.000000    NaN
        #11 2018-01-05 2018-01-05 23:58:59  47.766666  16.766666     117.0  AT0002R     0   7.730000    NaN
        #12 2018-01-08 2018-01-08 23:58:59  47.766666  16.766666     117.0  AT0002R     0   4.600000    NaN
        #13 2018-01-11 2018-01-11 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.490000    NaN
        #14 2018-01-14 2018-01-14 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.750000    NaN
        #15 2018-01-17 2018-01-17 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.000000    NaN
        #16 2018-01-20 2018-01-20 23:58:59  47.766666  16.766666     117.0  AT0002R     0   3.700000    NaN
        #17 2018-01-29 2018-01-29 23:58:59  47.766666  16.766666     117.0  AT0002R     0   6.990000    NaN
        #18 2018-02-01 2018-02-01 23:58:59  47.766666  16.766666     117.0  AT0002R     0   5.340000    NaN
        #19 2018-02-04 2018-02-04 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.620000    NaN
        #20 2018-02-07 2018-02-07 23:58:59  47.766666  16.766666     117.0  AT0002R     0   5.230000    NaN
        #21 2018-02-10 2018-02-10 23:58:59  47.766666  16.766666     117.0  AT0002R     0   6.230000    NaN
        #22 2018-02-13 2018-02-13 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.550000    NaN
        #23 2018-02-16 2018-02-16 23:58:59  47.766666  16.766666     117.0  AT0002R     0   8.220000    NaN
        #24 2018-02-19 2018-02-19 23:58:59  47.766666  16.766666     117.0  AT0002R     0        NaN    NaN
        #25 2018-02-22 2018-02-22 23:58:59  47.766666  16.766666     117.0  AT0002R     0        NaN    NaN
        #26 2018-02-25 2018-02-25 23:58:59  47.766666  16.766666     117.0  AT0002R     0   7.090000    NaN
        #27 2018-02-28 2018-02-28 23:58:59  47.766666  16.766666     117.0  AT0002R     0        NaN    NaN
        #28 2018-03-03 2018-03-03 23:58:59  47.766666  16.766666     117.0  AT0002R     0  17.110001    NaN
        #29 2018-03-06 2018-03-06 23:58:59  47.766666  16.766666     117.0  AT0002R     0  10.820000    NaN
        #30 2018-03-09 2018-03-09 23:58:59  47.766666  16.766666     117.0  AT0002R     0   5.670000    NaN
        #31 2018-03-12 2018-03-12 23:58:59  47.766666  16.766666     117.0  AT0002R     0   2.140000    NaN
        #