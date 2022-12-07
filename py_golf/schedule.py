"""
schedule.py

This script contains the functionality
to pull PGA Tour schedule data
"""

from utils import api_call

import pandas as pd

URL = "https://statdata-api-prod.pgatour.com/api/clientfile/HistoricalSchedules"

class Schedule:
    """ The Schedule class contains all resources needed
    to use the schedule-related API calls.

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
                 resp_format="json"):

        api_resp = api_call(URL, params={"userTrackingId": user_tracking_id,
                                         "T_CODE": t_code,
                                         "Year": year,
                                         "format": resp_format})
        schedule_df = pd.DataFrame(api_resp["data"])

        schedule_df = schedule_df.rename(
            columns = {
                "ID": "tournament_id",
                "TOURCODE": "tour_id",
                "PERM_NUM": "event_id",
                "YEAR": "year",
                "START_DATE": "start_date",
                "END_DATE": "end_date",
                "NAME": "event_name",
                "PURSE": "purse",
                "WEEK_NUMBER": "week_number",
                "SEQUENCE_NUMBER": "sequence_number",
                "TRN_TYPE": "tournament_type",
                "SCORED": "scored",
                "FORMAT": "play_format",
                "COURSE_NAME": "course_name",
                "CITY": "city",
                "STATE": "state",
                "COUNTRY": "country",
                "FIRST_NAME": "winner_first_name",
                "LAST_NAME": "winner_last_name",
                "FEDEX_POINTS_EARNED": "fedex_points_earned",
                "COURSE_NUMBER": "course_number",
                "MONEY_EARNED": "money_earned",
                "TEAM_COUNTRY": "team_country"
            }
            )

        schedule_df = schedule_df[[x for x in list(schedule_df) if x != "winners"]]

        self.data = schedule_df
