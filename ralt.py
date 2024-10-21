from utils.relalt import get_relative_altitude

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
print(f"Relative height of Galdhøpiggen: {get_relative_altitude(61.636471, 8.312443, altitude=2468):.2f} meters")

