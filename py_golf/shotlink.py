""" shotlink.py

This script contains the functionality
to pull shotlink data for a given group
"""

from utils import api_call
import shotlink_utils as s_utils

import pandas as pd

URL = "https://tourcastdata.pgatour.com/{t_code}/{event_id}/{year}/{course_id}/{round_num}/{hole}/{group}/holeview.json"

class Shotlink:
    """ The Shotlink class contains all resources needed
    to use the shotlink-related API calls.

    @param **t_code** (*str*): Tour code for which the schedule is
        desired. Valid values include:

        - 'r': PGA Tour
        - 's': Champions Tour
        - 'h': Korn Ferry Tour
        - 'm': Latinoamerica Tour
        - 'c': Canada Tour
    @param **event_id** (*int*): Unique identifier for the event of interest
    @param **year** (*int*): Year in YYYY format for which the schedule
        is desired. The schedule must be set or have been played to not
        return an error
    @param **course_id** (*int*): Unique identifier for the course of interest
    @param **round_num** (*int*): Unique identifier for the round within a specific
    	tournament at a specific course
    @param **hole** (*int*): Hole number within a round
    @param **group** (*int*): Unique identifier for the group of golfers

    Attributes:

        **data** (*pd.DataFrame*): DataFrame of the requested tour schedule
    """

    def __init__(self, t_code="r", year="2023",
                 event_id="002", course_id="704",
                 round_num="1", hole="18", group="12"):

        url = URL.format(t_code=t_code, event_id=event_id, year=year, course_id=course_id,
        	             round_num=round_num, hole=hole, group=group)
        api_resp = api_call(url, params={})

        self.api_resp = api_resp

        self.shots = s_utils.get_shot_information(api_resp)
