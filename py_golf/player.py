"""
player.py

This script contains the functionality
to pull PGA Tour player data
"""

from .utils import api_call

import pandas as pd

URL = "https://statdata.pgatour.com/players/player.json"

class Player:
    """ The Player class contains all resources needed
    to use the player-related API calls.

    @param **user_tracking_id** (*str*): Tracking ID necessary for
        downloading data from pgatour.com

    Attributes:

        **data** (*pd.DataFrame*): DataFrame of the player metadata
    """

    def __init__(self, user_tracking_id):

        api_resp = api_call(URL, params={"userTrackingId": user_tracking_id})

        player_df = pd.DataFrame(api_resp["plrs"])
        player_df["min_year"] = [min(x) for x in player_df["yrs"]]
        player_df["max_year"] = [max(x) for x in player_df["yrs"]]

        player_df = player_df.rename(
            columns = {
                "pid": "player_id",
                "nameF": "first_name",
                "nameL": "last_name",
                "ct": "country",
                "pr": "present_tour",
                "r": "pga_tour",
                "s": "champions_tour",
                "h": "korn_ferry_tour",
                "m": "latinoamerica_tour",
                "c": "canada_tour",
            }
            )

        player_df = player_df[["player_id",
                               "first_name",
                               "last_name",
                               "country",
                               "min_year",
                               "max_year",
                               "present_tour",
                               "pga_tour",
                               "champions_tour",
                               "korn_ferry_tour",
                               "latinoamerica_tour",
                               "canada_tour"]]

        self.data = player_df
