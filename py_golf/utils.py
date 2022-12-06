"""
utils.py

Utilities for the py_golf package
"""

from requests import get

def api_call(url, params):
    """ This function completes the API call at the given
    URL with the provided parameters.

    Args:
        - @param **url** (*str*): URL of the endpoint
        	of interest
        - @param **params** (*str*): Dictionary of endpoint
        	parameters

    Returns:
        - json_resp: JSON object of the API response
    """

    api_response = get(url, params=params)

    api_response.raise_for_status()
    json_resp = api_response.json()

    api_response.close()
    return json_resp
