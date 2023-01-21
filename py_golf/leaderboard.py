"""
leaderboard.py

This script contains the functionality
to pull leaderboard data for a given tournamnet
"""

from .utils import api_call
import leaderboard_utils as l_utils

import pandas as pd

URL = "https://statdata.pgatour.com/{t_code}/{event_id}/{year}/leaderboard-v2.json"

class Leaderboard:
    """ The Leaderboard class contains all resources needed
    to use the leaderboard-related API calls.

    @param **user_tracking_id** (*str*): Tracking ID necessary for
        downloading data from pgatour.com
    @param **t_code** (*str*): Tour code for which the schedule is
        desired. Valid values include:

        - 'r': PGA Tour
        - 's': Champions Tour
        - 'h': Korn Ferry Tour
        - 'm': Latinoamerica Tour
        - 'c': Canada Tour
    @param **year** (*int*): Year in YYYY format for which the schedule
        is desired. The schedule must be set or have been played to not
        return an error
    @param **resp_format** (*str*): Format for the data to be returned

    Attributes:

        **data** (*pd.DataFrame*): DataFrame of the requested tour schedule
    """

    def __init__(self, user_tracking_id,
                 t_code="r", year="2022",
                 event_id="493"):

        url = URL.format(t_code=t_code, event_id=event_id, year=year)
        api_resp = api_call(url, params={"userTrackingId": user_tracking_id})

        self.api_resp = api_resp

        self.holes = l_utils.get_hole_information(api_resp["leaderboard"])
        self.players = l_utils.get_player_information(api_resp["leaderboard"])
        self.shots = l_utils.get_shot_information(api_resp["leaderboard"])
