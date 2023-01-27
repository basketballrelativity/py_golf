"""
scorecard_utils.py

This script contains the functions
to help distill scorecard data from
the API response
"""

from typing import Dict

import pandas as pd

def process_ball_trajectory(ball: Dict) -> pd.DataFrame:
	""" This function processes ball trajectory information
	and stores it in a flat structure

	@param ball (dict): JSON object of ball trajectory data

	Returns:

		- ball_df (pd.DataFrame): DataFrame of ball trajectory information
	"""

	ball_df = pd.DataFrame(
		{"kind": [ball["kind"]],
		 "spin_rate_coef_0": [None if len(ball["spinRateFit"]) < 1 else ball["spinRateFit"][0]],
		 "spin_rate_coef_1": [None if len(ball["spinRateFit"]) < 2 else ball["spinRateFit"][1]],
		 "spin_rate_coef_2": [None if len(ball["spinRateFit"]) < 3 else ball["spinRateFit"][2]],
		 "spin_rate_coef_3": [None if len(ball["spinRateFit"]) < 4 else ball["spinRateFit"][3]],
		 "time_interval_start": [None if len(ball["timeInterval"]) < 1 else ball["timeInterval"][0]],
		 "time_interval_end": [None if len(ball["timeInterval"]) < 2 else ball["timeInterval"][1]],
		 "measured_time_interval_start": [None if len(ball["measuredTimeInterval"]) < 1 else ball["measuredTimeInterval"][0]],
		 "measured_time_interval_end": [None if len(ball["measuredTimeInterval"]) < 2 else ball["measuredTimeInterval"][1]],
		 "valid_time_interval_start": [None if len(ball["validTimeInterval"]) < 1 else ball["validTimeInterval"][0]],
		 "valid_time_interval_end": [None if len(ball["validTimeInterval"]) < 2 else ball["validTimeInterval"][1]],
		}
		)

	for dim in ["x", "y", "z"]:
		for order in range(1, 8):
			ball_df[dim + "_fit_" + str(order)] = [None if len(ball[dim + "Fit"]) < order else ball[dim + "Fit"][order-1]]

	return ball_df


def get_shot_information(group_json: Dict) -> pd.DataFrame:
	""" This function extracts shot-level information for
	a given player at a given tournament

	@param group_json (dict): Dictionary containing shotlink
		information from the API response

	Returns:

		- shot_df (pd.DataFrame): DataFrame containing shot-level
			information for a given player at a tournament
	"""

	players = len(group_json["groupDetails"])
	shot_df = pd.DataFrame()

	# Loop through rounds
	for player in range(players):
		hole = group_json["groupDetails"][player]
		hole_df = pd.DataFrame(hole["shots"])

		if "radarData" in list(hole_df):
			del hole_df["radarData"]

		shots_df = pd.DataFrame()
		for shot in hole["shots"]:
			print(shot)
			if "radarData" in shot:
				if pd.notnull(shot["radarData"]["strokeId"]):
					radar_df = pd.DataFrame(shot["radarData"])
					ball = shot["radarData"]["ballTrajectory"]
					if len(ball) > 0:
						ball_df = process_ball_trajectory(shot["radarData"]["ballTrajectory"][0])
					else:
						ball_df = pd.DataFrame()

					ball_df["strokeId"] = [shot["strokeId"]]

					del radar_df["ballTrajectory"]

					ball_df = ball_df.merge(radar_df, on="strokeId")
					shots_df = pd.concat([shots_df, ball_df])
				else:
					ball_df = pd.DataFrame({"strokeId": [shot["strokeId"]]})
					shots_df = pd.concat([shots_df, ball_df])
			else:
				ball_df = pd.DataFrame({"strokeId": [shot["strokeId"]]})
				shots_df = pd.concat([shots_df, ball_df])

		hole_df = hole_df.merge(shots_df, on="strokeId")
		hole_df["player_id"] = hole["playerId"]
		hole_df["group_id"] = hole["groupId"]
		hole_df["first_name"] = hole["firstName"]
		hole_df["last_name"] = hole["lastName"]
		hole_df["text_score"] = hole["textScore"]
		hole_df["round_score"] = hole["roundScore"]
		hole_df["total_score"] = hole["totalScore"]
		hole_df["strokes_behind"] = hole["strokesBehind"]
		hole_df["thru"] = hole["thru"]

		shot_df = pd.concat([shot_df, hole_df])

	shot_df["t_code"] = group_json["tourCode"]
	shot_df["event_id"] = group_json["tournamentNumber"]
	shot_df["year"] = group_json["seasonYear"]
	shot_df["round_num"] = group_json["roundNumber"]
	shot_df["course"] = group_json["courseNumber"]
	shot_df["hole"] = group_json["holeNumber"]
	shot_df["tee_time"] = group_json["teeTime"]
	shot_df["group_id"] = group_json["groupId"]

	return shot_df
