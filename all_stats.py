import pprint
import logging
from utils import fetch_json

logger = logging.getLogger(__name__)

PROJECT = "rv5_series"
EXPERIMENT = "DSemep"
LAYER = "Surface"
# True: Use aeroval-test API. False: Use aeroval API.
USE_AEROVAL_TEST = True

# User namespace on aeroval-test
DATAPATH = "davids"  # Data Path value used only for aeroval-test.


def process_menu(project: str, experiment: str) -> dict:
    """
    Returns details about varnames, obsnetworks and models parsed from
    the menu file for an experiment as a dict.
    """
    menu = fetch_json(f"/menu/{project}/{experiment}", aeroval_test=USE_AEROVAL_TEST, user_name_space=DATAPATH)

    var_names = list(menu)
    obs_networks = list(menu[var_names[0]]["obs"])
    models = list(menu[var_names[0]]["obs"][obs_networks[0]][LAYER])
    return {"varnames": var_names, "obsnetworks": obs_networks, "models": models}


def fetch_heatmap(
    project: str, experiment: str, frequency: str, region: str, period: str
) -> dict:
    return fetch_json(f"/heatmap/{project}/{experiment}/{frequency}/{region}/{period}", aeroval_test=USE_AEROVAL_TEST, user_name_space=DATAPATH)


def filter_heatmap(
    data,
    obsnetwork: str,
    model: str,
    varname: str,
    region: str,
    period: str,
    season: str,
):
    try:
        data = data[varname][obsnetwork][LAYER][model][varname][region][
            f"{period}-{season}"
        ]
    except:
        data = {}

    return data


if __name__ == "__main__":
    menu = process_menu(PROJECT, EXPERIMENT)

    data = fetch_heatmap(PROJECT, EXPERIMENT, "monthly", "ALL", "2022-all")

    result = {}
    for var in menu["varnames"]:
        result[var] = {}
        for obsnetwork in menu["obsnetworks"]:
            result[var][obsnetwork] = {}
            for mod in menu["models"]:
                result[var][obsnetwork][mod] = filter_heatmap(
                    data, obsnetwork, mod, var, "ALL", "2022", "all"
                )


    # result is now a nested dict with the stats values found here: https://aeroval-test.met.no/davids/pages/overall/?project=rv5_series&experiment=DSemep&season=All&region=ALL
    # Individual stats can be accessed as follows: result[varname][obsnetwork][model]["R"]
    print(f"Stats names: {list(result['concNno']['EBAS-m']['v5.3'])}")

    pprint.pprint(result["concNno"])
# OUTPUT:
# Stats names: ['totnum', 'weighted', 'num_valid', 'refdata_mean', 'refdata_std', 'data_mean', 'data_std', 'rms', 'nmb', 'mnmb', 'mb', 'mab', 'fge', 'R', 'R_spearman', 'R_kendall', 'num_coords_tot', 'num_coords_with_data', 'R_spatial_mean', 'R_temporal_median']
# {'EBAS-d': {'v5.0': {'R': 0.588441,
#                     'R_kendall': 0.577755,
#                     'R_spatial_mean': 0.671487,
#                     'R_spearman': 0.761363,
#                     'R_temporal_median': 0.6627809612990678,
#                     'data_mean': 0.37567,
#                     'data_std': 0.61095,
#                     'fge': 0.635292,
#                     'mab': 0.252253,
#                     'mb': -0.054032,
#                     'mnmb': -0.339667,
#                     'nmb': -0.125743,
#                     'num_coords_tot': 46.0,
#                     'num_coords_with_data': 41.0,
#                     'num_valid': 481.0,
#                     'refdata_mean': 0.429702,
#                     'refdata_std': 0.644235,
#                     'rms': 0.572716,
#                     'totnum': 552.0,
#                     'weighted': 0.0},
#            'v5.3': {'R': 0.583698,
#                     'R_kendall': 0.573926,
#                     'R_spatial_mean': 0.671963,
#                     'R_spearman': 0.758145,
#                     'R_temporal_median': 0.6218268784606572,
#                     'data_mean': 0.372037,
#                     'data_std': 0.600496,
#                     'fge': 0.640128,
#                     'mab': 0.254091,
#                     'mb': -0.057666,
#                     'mnmb': -0.345891,
#                     'nmb': -0.134199,
#                     'num_coords_tot': 46.0,
#                     'num_coords_with_data': 41.0,
#                     'num_valid': 481.0,
#                     'refdata_mean': 0.429702,
#                     'refdata_std': 0.644235,
#                     'rms': 0.572136,
#                     'totnum': 552.0,
#                     'weighted': 0.0},
#            'v5.3depNO3': {'R': 0.583695,
#                           'R_kendall': 0.573943,
#                           'R_spatial_mean': 0.671961,
#                           'R_spearman': 0.75817,
#                           'R_temporal_median': 0.6218146452137793,
#                           'data_mean': 0.372047,
#                           'data_std': 0.600482,
#                           'fge': 0.640114,
#                           'mab': 0.254089,
#                           'mb': -0.057655,
#                           'mnmb': -0.345842,
#                           'nmb': -0.134175,
#                           'num_coords_tot': 46.0,
#                           'num_coords_with_data': 41.0,
#                           'num_valid': 481.0,
#                           'refdata_mean': 0.429702,
#                           'refdata_std': 0.644235,
#                           'rms': 0.572132,
#                           'totnum': 552.0,
#                           'weighted': 0.0},
#            'v5.3mars': {'R': 0.583977,
#                         'R_kendall': 0.574134,
#                         'R_spatial_mean': 0.672163,
#                         'R_spearman': 0.758337,
#                         'R_temporal_median': 0.6212770319431414,
#                         'data_mean': 0.37116,
#                         'data_std': 0.599162,
#                         'fge': 0.640549,
#                         'mab': 0.253737,
#                         'mb': -0.058543,
#                         'mnmb': -0.347694,
#                         'nmb': -0.136241,
#                         'num_coords_tot': 46.0,
#                         'num_coords_with_data': 41.0,
#                         'num_valid': 481.0,
#                         'refdata_mean': 0.429702,
#                         'refdata_std': 0.644235,
#                         'rms': 0.571515,
#                         'totnum': 552.0,
#                         'weighted': 0.0},
#            'v5.3retro3b': {'R': 0.584234,
#                            'R_kendall': 0.574515,
#                            'R_spatial_mean': 0.672136,
#                            'R_spearman': 0.758594,
#                            'R_temporal_median': 0.6198620704524342,
#                            'data_mean': 0.372554,
#                            'data_std': 0.601831,
#                            'fge': 0.638788,
#                            'mab': 0.253821,
#                            'mb': -0.057148,
#                            'mnmb': -0.344042,
#                            'nmb': -0.132994,
#                            'num_coords_tot': 46.0,
#                            'num_coords_with_data': 41.0,
#                            'num_valid': 481.0,
#                            'refdata_mean': 0.429702,
#                            'refdata_std': 0.644235,
#                            'rms': 0.572247,
#                            'totnum': 552.0,
#                            'weighted': 0.0},
#            'v5.3retro3hmix': {'R': 0.568915,
#                               'R_kendall': 0.561192,
#                               'R_spatial_mean': 0.673494,
#                               'R_spearman': 0.746131,
#                               'R_temporal_median': 0.5541974130084466,
#                               'data_mean': 0.240764,
#                               'data_std': 0.37839,
#                               'fge': 0.766635,
#                               'mab': 0.255075,
#                               'mb': -0.188938,
#                               'mnmb': -0.630638,
#                               'nmb': -0.439696,
#                               'num_coords_tot': 46.0,
#                               'num_coords_with_data': 41.0,
#                               'num_valid': 481.0,
#                               'refdata_mean': 0.429702,
#                               'refdata_std': 0.644235,
#                               'rms': 0.562623,
#                               'totnum': 552.0,
#                               'weighted': 0.0}},
# 'EBAS-m': {'v5.0': {'R': 0.584154,
#                     'R_kendall': 0.577322,
#                     'R_spatial_mean': 0.667646,
#                     'R_spearman': 0.760984,
#                     'R_temporal_median': 0.6486062691740824,
#                     'data_mean': 0.373303,
#                     'data_std': 0.595434,
#                     'fge': 0.63615,
#                     'mab': 0.253154,
#                     'mb': -0.056399,
#                     'mnmb': -0.340807,
#                     'nmb': -0.131252,
#                     'num_coords_tot': 46.0,
#                     'num_coords_with_data': 41.0,
#                     'num_valid': 481.0,
#                     'refdata_mean': 0.429702,
#                     'refdata_std': 0.644235,
#                     'rms': 0.569736,
#                     'totnum': 552.0,
#                     'weighted': 0.0},
#            'v5.3': {'R': 0.579231,
#                     'R_kendall': 0.573579,
#                     'R_spatial_mean': 0.668341,
#                     'R_spearman': 0.758066,
#                     'R_temporal_median': 0.6149794945690563,
#                     'data_mean': 0.369762,
#                     'data_std': 0.586038,
#                     'fge': 0.640936,
#                     'mab': 0.255144,
#                     'mb': -0.05994,
#                     'mnmb': -0.347005,
#                     'nmb': -0.139493,
#                     'num_coords_tot': 46.0,
#                     'num_coords_with_data': 41.0,
#                     'num_valid': 481.0,
#                     'refdata_mean': 0.429702,
#                     'refdata_std': 0.644235,
#                     'rms': 0.569824,
#                     'totnum': 552.0,
#                     'weighted': 0.0},
#            'v5.3depNO3': {'R': 0.579227,
#                           'R_kendall': 0.57351,
#                           'R_spatial_mean': 0.668339,
#                           'R_spearman': 0.758027,
#                           'R_temporal_median': 0.6149280108085321,
#                           'data_mean': 0.369772,
#                           'data_std': 0.586026,
#                           'fge': 0.640922,
#                           'mab': 0.255142,
#                           'mb': -0.05993,
#                           'mnmb': -0.346957,
#                           'nmb': -0.139469,
#                           'num_coords_tot': 46.0,
#                           'num_coords_with_data': 41.0,
#                           'num_valid': 481.0,
#                           'refdata_mean': 0.429702,
#                           'refdata_std': 0.644235,
#                           'rms': 0.569821,
#                           'totnum': 552.0,
#                           'weighted': 0.0},
#            'v5.3mars': {'R': 0.579506,
#                         'R_kendall': 0.573545,
#                         'R_spatial_mean': 0.668526,
#                         'R_spearman': 0.758147,
#                         'R_temporal_median': 0.6141848629874206,
#                         'data_mean': 0.368885,
#                         'data_std': 0.584715,
#                         'fge': 0.641339,
#                         'mab': 0.254791,
#                         'mb': -0.060817,
#                         'mnmb': -0.34882,
#                         'nmb': -0.141533,
#                         'num_coords_tot': 46.0,
#                         'num_coords_with_data': 41.0,
#                         'num_valid': 481.0,
#                         'refdata_mean': 0.429702,
#                         'refdata_std': 0.644235,
#                         'rms': 0.569242,
#                         'totnum': 552.0,
#                         'weighted': 0.0},
#            'v5.3retro3b': {'R': 0.57974,
#                            'R_kendall': 0.573579,
#                            'R_spatial_mean': 0.668475,
#                            'R_spearman': 0.75811,
#                            'R_temporal_median': 0.616370442710962,
#                            'data_mean': 0.370266,
#                            'data_std': 0.587279,
#                            'fge': 0.63961,
#                            'mab': 0.254895,
#                            'mb': -0.059437,
#                            'mnmb': -0.345181,
#                            'nmb': -0.13832,
#                            'num_coords_tot': 46.0,
#                            'num_coords_with_data': 41.0,
#                            'num_valid': 481.0,
#                            'refdata_mean': 0.429702,
#                            'refdata_std': 0.644235,
#                            'rms': 0.569898,
#                            'totnum': 552.0,
#                            'weighted': 0.0},
#            'v5.3retro3hmix': {'R': 0.565257,
#                               'R_kendall': 0.561279,
#                               'R_spatial_mean': 0.670906,
#                               'R_spearman': 0.746299,
#                               'R_temporal_median': 0.5538195536461109,
#                               'data_mean': 0.238883,
#                               'data_std': 0.367038,
#                               'fge': 0.766643,
#                               'mab': 0.255369,
#                               'mb': -0.19082,
#                               'mnmb': -0.631704,
#                               'nmb': -0.444074,
#                               'num_coords_tot': 46.0,
#                               'num_coords_with_data': 41.0,
#                               'num_valid': 481.0,
#                               'refdata_mean': 0.429702,
#                               'refdata_std': 0.644235,
#                               'rms': 0.564666,
#                               'totnum': 552.0,
#                               'weighted': 0.0}}}
#
