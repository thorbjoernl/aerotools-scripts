# Tutorials / Scripts for Interfacing with Aeroval

This repo contains a number of collected scripts showing how to work with the [Aeroval](https://aeroval.met.no/) API, performing colocation and interpolation with Pyaerocom, reading EBAS data and more.

## Running the scripts
**TODO**: Make sure requirments.txt is updated.

- `pip install -r requirements.txt` (It is recommended to use a virtual environment)
- `python NAME_OF_SCRIPT`

## `all_stats.py`
This script fetches the statistics for the Project/Experiment combo. The returned data is nested dictionary with the stats for each obs_network-model combinatio:

<details>
    <summary>
        Example Output
    </summary>

```
    {'EBAS-d': {'v5.0': {'R': 0.588441,
                         'R_kendall': 0.577755,
                         'R_spatial_mean': 0.671487,
                         'R_spearman': 0.761363,
                         'R_temporal_median': 0.6627809612990678,
                         'data_mean': 0.37567,
                         'data_std': 0.61095,
                         'fge': 0.635292,
                         'mab': 0.252253,
                         'mb': -0.054032,
                         'mnmb': -0.339667,
                         'nmb': -0.125743,
                         'num_coords_tot': 46.0,
                         'num_coords_with_data': 41.0,
                         'num_valid': 481.0,
                         'refdata_mean': 0.429702,
                         'refdata_std': 0.644235,
                         'rms': 0.572716,
                         'totnum': 552.0,
                         'weighted': 0.0},
                'v5.3': {'R': 0.583698,
                         'R_kendall': 0.573926,
                         'R_spatial_mean': 0.671963,
                         'R_spearman': 0.758145,
                         'R_temporal_median': 0.6218268784606572,
                         'data_mean': 0.372037,
                         'data_std': 0.600496,
                         'fge': 0.640128,
                         'mab': 0.254091,
                         'mb': -0.057666,
                         'mnmb': -0.345891,
                         'nmb': -0.134199,
                         'num_coords_tot': 46.0,
                         'num_coords_with_data': 41.0,
                         'num_valid': 481.0,
                         'refdata_mean': 0.429702,
                         'refdata_std': 0.644235,
                         'rms': 0.572136,
                         'totnum': 552.0,
                         'weighted': 0.0},
                'v5.3depNO3': {'R': 0.583695,
                               'R_kendall': 0.573943,
                               'R_spatial_mean': 0.671961,
                               'R_spearman': 0.75817,
                               'R_temporal_median': 0.6218146452137793,
                               'data_mean': 0.372047,
                               'data_std': 0.600482,
                               'fge': 0.640114,
                               'mab': 0.254089,
                               'mb': -0.057655,
                               'mnmb': -0.345842,
                               'nmb': -0.134175,
                               'num_coords_tot': 46.0,
                               'num_coords_with_data': 41.0,
                               'num_valid': 481.0,
                               'refdata_mean': 0.429702,
                               'refdata_std': 0.644235,
                               'rms': 0.572132,
                               'totnum': 552.0,
                               'weighted': 0.0},
                'v5.3mars': {'R': 0.583977,
                             'R_kendall': 0.574134,
                             'R_spatial_mean': 0.672163,
                             'R_spearman': 0.758337,
                             'R_temporal_median': 0.6212770319431414,
                             'data_mean': 0.37116,
                             'data_std': 0.599162,
                             'fge': 0.640549,
                             'mab': 0.253737,
                             'mb': -0.058543,
                             'mnmb': -0.347694,
                             'nmb': -0.136241,
                             'num_coords_tot': 46.0,
                             'num_coords_with_data': 41.0,
                             'num_valid': 481.0,
                             'refdata_mean': 0.429702,
                             'refdata_std': 0.644235,
                             'rms': 0.571515,
                             'totnum': 552.0,
                             'weighted': 0.0},
                'v5.3retro3b': {'R': 0.584234,
                                'R_kendall': 0.574515,
                                'R_spatial_mean': 0.672136,
                                'R_spearman': 0.758594,
                                'R_temporal_median': 0.6198620704524342,
                                'data_mean': 0.372554,
                                'data_std': 0.601831,
                                'fge': 0.638788,
                                'mab': 0.253821,
                                'mb': -0.057148,
                                'mnmb': -0.344042,
                                'nmb': -0.132994,
                                'num_coords_tot': 46.0,
                                'num_coords_with_data': 41.0,
                                'num_valid': 481.0,
                                'refdata_mean': 0.429702,
                                'refdata_std': 0.644235,
                                'rms': 0.572247,
                                'totnum': 552.0,
                                'weighted': 0.0},
                'v5.3retro3hmix': {'R': 0.568915,
                                   'R_kendall': 0.561192,
                                   'R_spatial_mean': 0.673494,
                                   'R_spearman': 0.746131,
                                   'R_temporal_median': 0.5541974130084466,
                                   'data_mean': 0.240764,
                                   'data_std': 0.37839,
                                   'fge': 0.766635,
                                   'mab': 0.255075,
                                   'mb': -0.188938,
                                   'mnmb': -0.630638,
                                   'nmb': -0.439696,
                                   'num_coords_tot': 46.0,
                                   'num_coords_with_data': 41.0,
                                   'num_valid': 481.0,
                                   'refdata_mean': 0.429702,
                                   'refdata_std': 0.644235,
                                   'rms': 0.562623,
                                   'totnum': 552.0,
                                   'weighted': 0.0}},
     'EBAS-m': {'v5.0': {'R': 0.584154,
                         'R_kendall': 0.577322,
                         'R_spatial_mean': 0.667646,
                         'R_spearman': 0.760984,
                         'R_temporal_median': 0.6486062691740824,
                         'data_mean': 0.373303,
                         'data_std': 0.595434,
                         'fge': 0.63615,
                         'mab': 0.253154,
                         'mb': -0.056399,
                         'mnmb': -0.340807,
                         'nmb': -0.131252,
                         'num_coords_tot': 46.0,
                         'num_coords_with_data': 41.0,
                         'num_valid': 481.0,
                         'refdata_mean': 0.429702,
                         'refdata_std': 0.644235,
                         'rms': 0.569736,
                         'totnum': 552.0,
                         'weighted': 0.0},
                'v5.3': {'R': 0.579231,
                         'R_kendall': 0.573579,
                         'R_spatial_mean': 0.668341,
                         'R_spearman': 0.758066,
                         'R_temporal_median': 0.6149794945690563,
                         'data_mean': 0.369762,
                         'data_std': 0.586038,
                         'fge': 0.640936,
                         'mab': 0.255144,
                         'mb': -0.05994,
                         'mnmb': -0.347005,
                         'nmb': -0.139493,
                         'num_coords_tot': 46.0,
                         'num_coords_with_data': 41.0,
                         'num_valid': 481.0,
                         'refdata_mean': 0.429702,
                         'refdata_std': 0.644235,
                         'rms': 0.569824,
                         'totnum': 552.0,
                         'weighted': 0.0},
                'v5.3depNO3': {'R': 0.579227,
                               'R_kendall': 0.57351,
                               'R_spatial_mean': 0.668339,
                               'R_spearman': 0.758027,
                               'R_temporal_median': 0.6149280108085321,
                               'data_mean': 0.369772,
                               'data_std': 0.586026,
                               'fge': 0.640922,
                               'mab': 0.255142,
                               'mb': -0.05993,
                               'mnmb': -0.346957,
                               'nmb': -0.139469,
                               'num_coords_tot': 46.0,
                               'num_coords_with_data': 41.0,
                               'num_valid': 481.0,
                               'refdata_mean': 0.429702,
                               'refdata_std': 0.644235,
                               'rms': 0.569821,
                               'totnum': 552.0,
                               'weighted': 0.0},
                'v5.3mars': {'R': 0.579506,
                             'R_kendall': 0.573545,
                             'R_spatial_mean': 0.668526,
                             'R_spearman': 0.758147,
                             'R_temporal_median': 0.6141848629874206,
                             'data_mean': 0.368885,
                             'data_std': 0.584715,
                             'fge': 0.641339,
                             'mab': 0.254791,
                             'mb': -0.060817,
                             'mnmb': -0.34882,
                             'nmb': -0.141533,
                             'num_coords_tot': 46.0,
                             'num_coords_with_data': 41.0,
                             'num_valid': 481.0,
                             'refdata_mean': 0.429702,
                             'refdata_std': 0.644235,
                             'rms': 0.569242,
                             'totnum': 552.0,
                             'weighted': 0.0},
                'v5.3retro3b': {'R': 0.57974,
                                'R_kendall': 0.573579,
                                'R_spatial_mean': 0.668475,
                                'R_spearman': 0.75811,
                                'R_temporal_median': 0.616370442710962,
                                'data_mean': 0.370266,
                                'data_std': 0.587279,
                                'fge': 0.63961,
                                'mab': 0.254895,
                                'mb': -0.059437,
                                'mnmb': -0.345181,
                                'nmb': -0.13832,
                                'num_coords_tot': 46.0,
                                'num_coords_with_data': 41.0,
                                'num_valid': 481.0,
                                'refdata_mean': 0.429702,
                                'refdata_std': 0.644235,
                                'rms': 0.569898,
                                'totnum': 552.0,
                                'weighted': 0.0},
                'v5.3retro3hmix': {'R': 0.565257,
                                   'R_kendall': 0.561279,
                                   'R_spatial_mean': 0.670906,
                                   'R_spearman': 0.746299,
                                   'R_temporal_median': 0.5538195536461109,
                                   'data_mean': 0.238883,
                                   'data_std': 0.367038,
                                   'fge': 0.766643,
                                   'mab': 0.255369,
                                   'mb': -0.19082,
                                   'mnmb': -0.631704,
                                   'nmb': -0.444074,
                                   'num_coords_tot': 46.0,
                                   'num_coords_with_data': 41.0,
                                   'num_valid': 481.0,
                                   'refdata_mean': 0.429702,
                                   'refdata_std': 0.644235,
                                   'rms': 0.564666,
                                   'totnum': 552.0,
                                   'weighted': 0.0}}}
```

</details>

## `map_scatter.py`
Uses the *Aeroval* API to fetch scatter data for a given project,experiment combination.

<details>
    <summary>Example Output</summary>

```
{'altitude': 110.0,
 'latitude': 38.366667,
 'longtitude': 23.083333,
 'region': ['Greece'],
 'station_name': 'Aliartos',
 'statistics': {'R': None,
                'R_kendall': None,
                'R_spatial_mean': None,
                'R_spatial_median': None,
                'R_spearman': None,
                'R_temporal_mean': None,
                'R_temporal_median': None,
                'data_mean': None,
                'data_std': None,
                'fge': None,
                'mab': None,
                'mb': None,
                'mnmb': None,
                'nmb': None,
                'num_valid': None,
                'refdata_mean': None,
                'refdata_std': None,
                'rms': None,
                'totnum': None,
                'weighted': None}}
```

</details>

## `site_data.py`
Returns additional detail for EBAS stations by looking up additional metadata in the EBAS file index.

<details>
    <summary>Experiment Output</summary>

```
{'platform_code': 'GR0001S',
 'station_airs_id': None,
 'station_altitude': 110.0,
 'station_code': 'GR0001R',
 'station_gaw_id': None,
 'station_gaw_name': None,
 'station_gaw_type': None,
 'station_landuse': None,
 'station_latitude': 38.366667,
 'station_longitude': 23.083333,
 'station_name': 'Aliartos',
 'station_other_ids': None,
 'station_setting': None,
 'station_state_code': None,
 'station_wdca_id': None,
 'station_wmo_region': None}
```

</details>

## `ebas.py`
Illustrates how to load EBAS data into a pandas DataFrame using pyaro/pyaro-readers.

<details>
    <summary>Example Output</summary>

```
    start_time   end_time   latitude  ...  stdev_aerosol#sulphate_total#ug S/m3  value_aerosol#sulphate_total#ug m-3 stdev_aerosol#sulphate_total#ug m-3
0   2010-01-01 2010-01-02  47.766666  ...                                   NaN                                  NaN                                 NaN
1   2010-01-02 2010-01-03  47.766666  ...                                   NaN                                  NaN                                 NaN
2   2010-01-03 2010-01-04  47.766666  ...                                   NaN                                  NaN                                 NaN
3   2010-01-04 2010-01-05  47.766666  ...                                   NaN                                  NaN                                 NaN
4   2010-01-05 2010-01-06  47.766666  ...                                   NaN                                  NaN                                 NaN
..         ...        ...        ...  ...                                   ...                                  ...                                 ...
360 2010-12-27 2010-12-28  47.766666  ...                                   NaN                                  1.8                                 NaN
361 2010-12-28 2010-12-29  47.766666  ...                                   NaN                                  1.8                                 NaN
362 2010-12-29 2010-12-30  47.766666  ...                                   NaN                                  6.6                                 NaN
363 2010-12-30 2010-12-31  47.766666  ...                                   NaN                                  8.1                                 NaN
364 2010-12-31 2011-01-01  47.766666  ...                                   NaN                                  8.0                                 NaN

[365 rows x 11 columns]
```

</details>

## `ebas2.py`
Similarly shows how to use the Pyaerocom reader to read and filter EBAS data into a pandas DataFrame.

<details>
    <summary>Example Output</summary>

```
                      time      value matrix component        unit
214800 2011-01-01 00:30:00        NaN    air     ozone  nmol mol-1
214801 2011-01-01 01:29:59        NaN    air     ozone  nmol mol-1
214802 2011-01-01 02:29:59        NaN    air     ozone  nmol mol-1
214803 2011-01-01 03:30:00        NaN    air     ozone  nmol mol-1
214804 2011-01-01 04:29:59        NaN    air     ozone  nmol mol-1
...                    ...        ...    ...       ...         ...
223555 2011-12-31 19:29:59  21.576131    air     ozone  nmol mol-1
223556 2011-12-31 20:29:59  20.098314    air     ozone  nmol mol-1
223557 2011-12-31 21:30:00  19.802751    air     ozone  nmol mol-1
223558 2011-12-31 22:29:59  18.620497    air     ozone  nmol mol-1
223559 2011-12-31 23:29:59  18.324933    air     ozone  nmol mol-1

[8760 rows x 5 columns]
```

</details>