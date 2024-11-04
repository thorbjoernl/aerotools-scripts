from utils.relalt import get_relative_altitude
import statistics
# Uses default TOPO folder at /lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/nc
# Can override using the topodir argument, but currently this will only work for 
# GTOPO30, or very similarly structured datasets.
#
# A couple of notes / and limitations:
# - Distance is calculated based on the haversine formula.
# - Minimum altitude is currently capped at 0.
# - All elevation / distance units are in meters.
# - Some areas may not have data available (eg. in the middle of the ocean) and 
# will raise a ValueError.
# - The topo dataset is split into multiple files, and currently only the file which 
# encompasses the lat/lon point is used for calculation. May give unexpected values along boundaries.

# The following script calculates 3km relative elevation for the locations found in
# Klingberg et al. 2012, and compares the values with values provided in Table 1.
# Note that this paper uses the average (not minimum) elevation within the radius for
# comparison, and that the topography resolution they use is higher (50x50m)

TABLE_VALUES = [
    {
        "name": "Alafors",
        "latitude": 57.935000,
        "longitude": 12.119333,
        "altitude": 37,
        "relaltitude": -2
    },
    {
        "name": "Asa",
        "latitude": 57.164500,
        "longitude": 14.782667,
        "altitude": 179,
        "relaltitude": -20
    },
    {
        "name": "Brobacka",
        "latitude": 57.980667,
        "longitude": 12.460000,
        "altitude": 167,
        "relaltitude": 46
    },
    {
        "name": "Grimsö",
        "latitude": 59.727500,
        "longitude": 15.469000,
        "altitude": 105,
        "relaltitude": -13,
    },
    {
        "name": "Grytebergen",
        "latitude": 57.977167,
        "longitude": 12.364167,
        "altitude": 176,
        "relaltitude": 43
    },
    {
        "name": "Hedared",
        "latitude": 57.808333,
        "longitude": 12.747500,
        "altitude": 191,
        "relaltitude": -11
    },
    {
        "name": "Klevsjön",
        "latitude": 57.979333,
        "longitude": 12.378500,
        "altitude": 120,
        "relaltitude": -9
    },
    {
        "name": "Lanna",
        "latitude": 58.345333, 
        "longitude": 13.123833,
        "altitude": 74,
        "relaltitude": 2
    },
    {
        "name": "Nidingen",
        "latitude": 57.303500,
        "longitude": 11.905167,
        "altitude": 1,
        "relaltitude": 1
    },
    {
        "name": "Norra Kvill",
        "latitude": 57.810833,
        "longitude": 15.564667,
        "altitude": 251,
        "relaltitude": 62,

    },
    {
        "name": "Norr Malma",
        "latitude": 59.831667,
        "longitude": 18.631000,
        "altitude": 16,
        "relaltitude": 0
    },
    {
        "name": "Rönnäng",
        "latitude": 57.936167,
        "longitude": 11.583667,
        "altitude": 23,
        "relaltitude": 11
    },
    {
        "name": "Sandhult",
        "latitude": 57.760500,
        "longitude": 12.841167,
        "altitude": 296,
        "relaltitude": 38
    },
    {
        "name": "Vavihill",
        "latitude": 56.028000,
        "longitude": 13.149500,
        "altitude": 168,
        "relaltitude": 17,
    },
    {
        "name": "Östad",
        "latitude": 56.028000, 
        "longitude": 13.149500,
        "altitude": 63,
        "relaltitude": -23
    }

]


print(f"{'site'.rjust(15)} {'lat'.rjust(10)} {'lon'.rjust(10)} {'alt'.rjust(7)} {'ralt'.rjust(7)} {'exp ralt'.rjust(10)} {'delta'.rjust(7)}")
ls = []
for site in TABLE_VALUES:
    ralt = get_relative_altitude(site["latitude"], site["longitude"], radius=3000, fun="mean", altitude=site["altitude"], topodir="topo/nc2")

    delta = ralt - site["relaltitude"]
    ls.append(delta)
    print(f"{site['name'].rjust(15)} {str(round(site['latitude'], 4)).rjust(10)} {str(round(site['longitude'], 4)).rjust(10)} {str(round(site['altitude'], 2)).rjust(7)} {str(round(ralt, 2)).rjust(7)} {str(round(site['relaltitude'], 2)).rjust(10)} {str(round(delta, 2)).rjust(7)}")

print(statistics.mean(ls))