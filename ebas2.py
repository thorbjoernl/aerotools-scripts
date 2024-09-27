import pyaerocom as pya
import pandas as pd
import datetime
import numpy as np

def to_dataframe(ungridded: pya.ungriddeddata.UngriddedData) -> pd.DataFrame:
    """
    Produces a dataframe from a pyaerocom ungridded data object.
    """
    df = pd.DataFrame()
    # TODO: Find out how to prefilter this because this is pretty slow and memory intensive
    
    # Spatio-temporal information
    df["time"] = ungridded._data[:, ungridded._TIMEINDEX].astype("datetime64[s]")
    df["var_name"] = [list(ungridded.metadata[x]["var_info"].values())[0]["var_name"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    df["latitude"] = ungridded._data[:, ungridded._LATINDEX]
    df["longitude"] = ungridded._data[:, ungridded._LONINDEX]
    df["altitude"] = ungridded._data[:, ungridded._ALTITUDEINDEX]
    
    # Actual data values.
    df["value"] = ungridded._data[:, ungridded._DATAINDEX]
    # Currently I assume there is only one value in varinfo. Not sure if this assumption breaks in some cases.
    df["unit"] = [list(ungridded.metadata[x]["var_info"].values())[0]["units"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    
    # Add metadata.
    df["station_id"] = [ungridded.metadata[x]["station_id"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    df["station_name"] = [ungridded.metadata[x]["station_name"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    df["country_code"] = [ungridded.metadata[x]["country_code"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    df["country"] = [ungridded.metadata[x]["country"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    df["ts_type"] = [ungridded.metadata[x]["ts_type"] for x in ungridded._data[:, ungridded._METADATAKEYINDEX]]
    #

    # Available metadata keys are the following: 
    # They can be added to the dataframe following the examples above
    # ['latitude', 'longitude', 'altitude', 'filename', 'station_id', 'station_name', 'instrument_name', 'PI', 'country', 'country_code', 'ts_type', 'data_id', 'dataset_name', 'data_product', 'data_version', 'data_level', 'framework', 'instr_vert_loc', 'revision_date', 'website', 'ts_type_src', 'stat_merge_pref_attr', 'data_revision', 'var_info', 'variables']
    return df

if __name__ == "__main__":
    VAR = "vmro3max"

    obs_reader = pya.io.ReadUngridded("EBASMC")

    data = obs_reader.read(vars_to_retrieve=VAR)
    
    df = to_dataframe(data)


    # Don't think this is necessary but ensure ts_type is consistent.
    df = df[df["ts_type"] == "hourly"]

    # Filter for specific years.
    df = df[df["time"].dt.year.isin([2010, 2011])]

    # Filter for date range.
    start = datetime.datetime(2010, 3, 14, 12, 0, 0)
    end = datetime.datetime(2010, 4, 14, 12, 0, 0)
    df = df[np.logical_and(df["time"] >= start, df["time"] <= end)]

    # Ensure timeseries is sorted (may not be necessary)
    df.sort_values("time", ascending=True)

    # Select station
    df = df[df["station_id"] == "AM0001R"]
    #df = df[df["station_name"] == "Amberd"]

    print(df)