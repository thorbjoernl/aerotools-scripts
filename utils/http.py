import requests
import logging
import json


logger = logging.getLogger(__name__)

HTTP_OK = 200


def fetch_json(path: str, aeroval_test: bool = True, user_name_space: str | None = None) -> dict:
    """
    Helper function to fetch and parse json from some path on api.aeroval[-test].met.no.
    """
    if aeroval_test:
        url = f"https://api.aeroval-test.met.no/api/0.2.1{path}?data_path={user_name_space}"
    else:
        url = f"https://api.aeroval.met.no/api/0.2.1{path}"

    logger.info(f"Fetching data from '{url}'")
    r = requests.get(url)
    if r.status_code == HTTP_OK:
        return json.loads(r.content)
    else:
        logger.error(
            f"Fetching data from '{url}' failed with status code {r.status_code}"
        )
        return None