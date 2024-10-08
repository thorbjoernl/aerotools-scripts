import iris.analysis
import iris
import iris.cube
import pyaerocom as pya

if __name__ == "__main__":
    mod_reader = pya.io.mscw_ctm.reader.ReadMscwCtm(
        "EMEP",
        data_dir="/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/TRENDS/2020",
    )

    mod_data: pya.griddeddata.GriddedData = mod_reader.read_var("concnh3", ts_type="daily")

    obs_reader = pya.io.ReadUngridded("EBASMC")

    obs_data: pya.ungriddeddata.UngriddedData = obs_reader.read(
        vars_to_retrieve="concnh3",
        #ts_type="daily"
    )

    coord_pairs = obs_data._get_stat_coords()[1]
    lat, lon = list(zip(*coord_pairs))

    # lat and lon must be an ascending list with duplicates removed for interpolation to work as intended.
    lat = sorted(set(list(lat)))
    lon = sorted(set(list(lon)))

    mod_data_int = mod_data.interpolate(scheme=iris.analysis.Linear(), latitude=lat, longitude=lon)
    
    #result = pya.io.iris_io.concatenate_iris_cubes(cubes)

    colocated_data = pya.colocation.colocation_utils.colocate_gridded_ungridded(
        mod_data_int, obs_data
    )

    df = colocated_data.to_dataframe()
    print(df)
