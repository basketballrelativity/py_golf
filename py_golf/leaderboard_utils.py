"""
leaderboard_utils.py

This script contains the functions
to help distill leaderboard data from
the API response
"""

from typing import Dict

import pandas as pd

def get_hole_information(leader_json: Dict) -> pd.DataFrame:
	""" This function extracts hole-level information for
	a given tournament

	@param leader_json (dict): Dictionary containing leaderboard
		information from the API response

	Returns:

		- course_df (pd.DataFrame): DataFrame containing hole-level
			information for a given tournament
	"""

	courses = len(leader_json["courses"])
	course_df = pd.DataFrame()

	# Loop through courses
	for course in range(courses):
		course_json = leader_json["courses"][course]
		holes = course_json["holes"]

		# Loop through holes
		holes_df = pd.DataFrame()
		for hole in holes:

			hole_df = pd.DataFrame(hole["round"])
			hole_df["hole_id"] = hole["hole_id"]
			holes_df = pd.concat([holes_df, hole_df])

		holes_df["course_id"] = course_json["course_id"]

		course_df = pd.concat([course_df, holes_df])

	course_df["tournament_id"] = leader_json["tournament_id"]
	course_df["tour_code"] = leader_json["tour_code"]

	return course_df


def get_player_information(leader_json: Dict) -> pd.DataFrame:
	""" This function extracts player-level information for
	a given tournament

	@param leader_json (dict): Dictionary containing leaderboard
		information from the API response

	Returns:

		- player_df (pd.DataFrame): DataFrame containing player-level
			information for a given tournament
	"""

	columns_to_keep = ["player_id", "current_position", "start_position",
					   "thru", "back9", "start_hole", "course_id", "current_round", "course_hole",
					   "today", "total", "wildcard", "total_strokes", "group_id"]

	player_df = pd.DataFrame(leader_json["players"])[columns_to_keep]

	return player_df


def get_shot_information(leader_json: Dict) -> pd.DataFrame:
	""" This function extracts shot-level information for
	a given tournament

	@param leader_json (dict): Dictionary containing leaderboard
		information from the API response

	Returns:

		- shot_df (pd.DataFrame): DataFrame containing shot-level
			information for a given tournament
	"""

	players = len(leader_json["players"])
	shot_df = pd.DataFrame()

	# Loop through courses
	for player in range(players):
		player_json = leader_json["players"][player]
		holes = player_json["holes"]

		# Loop through holes
		holes_df = pd.DataFrame()
		for hole in holes:

			shots_df = pd.DataFrame(hole["shots"])
			shots_df["course_hole_id"] = hole["course_hole_id"]
			shots_df["par"] = hole["par"]
			holes_df = pd.concat([holes_df, shots_df])

		holes_df["player_id"] = player_json["player_id"]
		holes_df["course_id"] = player_json["course_id"]

		shot_df = pd.concat([shot_df, holes_df])

	shot_df["tournament_id"] = leader_json["tournament_id"]
	shot_df["tour_code"] = leader_json["tour_code"]

	return shot_df
