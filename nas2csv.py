import pyaerocom as pya
import pandas as pd
import pyaro


def read_ebas_data(file_name: str) -> pd.DataFrame | None:
    """
    Reads data from a single ebas .nas file providing it as a pandas data frame.
    The resulting column will contain data for separate components as two colums
    (one for the values and one for the standard deviations named 'value_{ebas_var}'
    and 'stdev_{ebas_var}'). ebas_var is the component name used by pyaro which is
    '{matrix}#{comp_name}#{unit}' (eg. 'precip#precipitation_amount#mm').
    """
    engines = pyaro.list_timeseries_engines()
    df = None
    with engines["nilupmfebas"].open(file_name) as ts:
        df = None
        for var in ts.variables():
            data: pyaro.timeseries.NpStructuredData = ts.data(var)
            new = pd.DataFrame(
                {
                    "start_time": data.start_times,
                    "end_time": data.end_times,
                    "latitude": data.latitudes,
                    "longitude": data.longitudes,
                    "altitude": data.altitudes,
                    "station": data.stations,
                    "flag": data.flags,
                    f"value_{var}": data.values,
                    f"stdev_{var}": data.standard_deviations,
                }
            )
            if df is None:
                df = new
            else:
                df = df.merge(
                    new,
                    on=(
                        "start_time",
                        "end_time",
                        "latitude",
                        "longitude",
                        "altitude",
                        "station",
                        "flag",
                    ),
                    how="outer",
                )
    if df is not None:
        df = df.sort_values("start_time")
    return df


if __name__ == "__main__":
    FILE = "NO0001R.20090101000000.20130101000000.uv_abs.ozone.air.1y.1h.NO01L_uv_abs_uk_0001.NO01L_uv_abs.lev2.nas"
    path = f"/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/{FILE}"

    data = read_ebas_data(path)

    data.to_csv("test.csv")
