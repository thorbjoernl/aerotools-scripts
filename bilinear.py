import iris.analysis
import iris
import iris.cube
import pyaerocom as pya

if __name__ == "__main__":
    obs_reader = pya.io.ReadUngridded("EBASMC")
    obs_data: pya.ungriddeddata.UngriddedData = obs_reader.read(
        vars_to_retrieve="vmro3",
        #ts_type="daily"
    )

    w = min(obs_data.longitude) ; e = max(obs_data.longitude) ; s = min(obs_data.latitude) ; n = max(obs_data.latitude)
    box = pya.utils.BoundingBox(west=w, east=e, south=s, north=n)

    mod_reader = pya.io.mscw_ctm.reader.ReadMscwCtm(
        "EMEP",
        data_dir="/lustre/storeB/project/fou/kl/emep/ModelRuns/2024TESTS/CAO4_series/EMEP0302c_n8rv5_4DS_CAO4nvdC_emis2015.2019", 
    )
    
    mod_data: pya.griddeddata.GriddedData = mod_reader.read_var("vmro3", ts_type="hourly", bounding_box = box)

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
