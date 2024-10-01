import iris.analysis
import iris
import pyaerocom as pya

if __name__ == "__main__":
    mod_reader = pya.io.mscw_ctm.reader.ReadMscwCtm(
        "EMEP",
        data_dir="/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/TRENDS/2020",
    )

    mod_data: pya.griddeddata.GriddedData = mod_reader.read_var("concnh3", "daily")

    obs_reader = pya.io.ReadUngridded("EBASMC")

    obs_data: pya.ungriddeddata.UngriddedData = obs_reader.read(
        vars_to_retrieve="concnh3"
    )

    coord_pairs = obs_data._get_stat_coords()[1]
    lat, lon = list(zip(*coord_pairs))
    # lat, lon = zip(*list(itertools.product(mod_data.cube.coord('latitude').points, mod_data.cube.coord('longitude').points)))
    mod_data.cube = mod_data.cube.interpolate(
        [("longitude", lon), ("latitude", lat)], iris.analysis.Linear()
    )
    colocated_data = pya.colocation.colocation_utils.colocate_gridded_ungridded(
        mod_data, obs_data
    )

    print(colocated_data)
