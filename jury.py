import difflib
import json
from datetime import datetime, timedelta
from typing import Dict
from Tio import Tio

questions = []
judgements = {}

# LOAD IN QUESTIONS
with open("questions/info.json") as info:
	info = json.load(info)
	for level in info["questions"]:
		level_questions = info["questions"][level]
		for question_name in level_questions:
			question_data = {}
			question_data["name"] = question_name
			question_data["number"] = len(questions)  # 0 indexed
			question_data["level"] = level
			question_data["penalty"] = info["penalties"][level]
			question_data["points"] = {}
			with open(f"questions/{question_name}/QUESTION.md", "r", encoding="UTF-8") as file:
				question_data["question"] = file.read()
			with open(f"questions/{question_name}/INPUT.txt", "r", encoding="UTF-8") as file:
				question_data["input"] = file.read()
			with open(f"questions/{question_name}/ANSWER.txt", "r", encoding="UTF-8") as file:
				question_data["answer"] = file.read()
			questions.append(question_data)

TIME_BEGIN = datetime.now().astimezone()
DURATION = timedelta(minutes=120)

def P_speed(submission_time: datetime) -> float:
	time_passed = submission_time - TIME_BEGIN
	points = 250 * (1 - time_passed/DURATION)
	return points

def P_efficiency(execution_time: int, question_number: int) -> float:
	least_execution_time = get_least_execution_time(question_number) or execution_time
	points = 250 * (least_execution_time/execution_time)
	return points

def P_total(question_number: int, submission_time: datetime, execution_time: int) -> float:
	points = P_speed(submission_time) + P_efficiency(execution_time, question_number)
	points = round(points, 2)
	return points

def get_least_execution_time(question_number: int) -> int:
	question = questions[question_number]
	least_execution_time = None
	for team in question["points"]:
		question_judgement = judgements[team][question_number]
		execution_time = question_judgement["execution_time"]
		if not least_execution_time or execution_time < least_execution_time:
			least_execution_time = execution_time
	return least_execution_time

def get_penalised_points(question_number: int) -> float:
	question = questions[question_number]
	points = question["points"].values()
	if len(points) == 0:
		return 0
	else:
		least_points = min(points)
		penalised = round(least_points - question["penalty"], 2)
		return max(0, penalised)

def get_leaderboard(include_points=True):
	'''Sorts the participants by their net points.'''
	global questions
	total_points = {team: 0 for team in judgements.keys()}

	for question in questions:
		# Record the slowest time for this question
		if len(question["points"]) == 0:
			# No one submitted, skip the question altogether
			continue

		for team in judgements.keys():
			if team in question["points"]:
				# Give them their points
				total_points[team] += question["points"][team]
			else:
				# They get the penalised points
				total_points[team] += get_penalised_points(question["number"])

	# Flatten and sort
	total_points = [{"team": team, "points": total_points[team]} for team in total_points]
	print(total_points)
	total_points.sort(key=lambda t: round(t["points"], 2), reverse=True)  # Sort by total points
	if not include_points:
		total_points = [t["team"] for t in total_points]  # Give a list of the teams only
	print("\t", total_points)
	return total_points

def get_first_line_of_difference(correct, wrong):
	correct_lines, wrong_lines = correct.split("\n"), wrong.split("\n")
	sequence = difflib.SequenceMatcher(None, correct_lines, wrong_lines)
	first_correct_lines = sequence.get_matching_blocks()[0].size
	return first_correct_lines + 1

site = Tio()
def judge(question_number: int, language: str, source_code: str, submission_time: datetime) -> Dict[str, any]:
	question = questions[question_number]
	request = site.new_request(language, source_code, question["input"])
	response = site.send(request)
	output = response.stdout
	passed = output.strip() == question["answer"].strip()
	execution_time = float(response.real_time)
	judgement = {
		"question_number": question_number,
		"code": source_code,
		"output": output,
		"passed": passed,
		"execution_time": execution_time,
		"submission_time": submission_time,
	}
	if not passed:
		# Diff solving
		correct_lines, wrong_lines = question["answer"].split("\n"), output.split("\n")
		sequence = difflib.SequenceMatcher(None, correct_lines, wrong_lines)
		lod = sequence.get_matching_blocks()[0].size + 1
		diff = {
			"lod": lod,
			"correct": correct_lines[lod-1],
			"wrong": wrong_lines[lod-1]
		}
		judgement["diff"] = diff
	if passed:
		judgement["points"] = P_total(question["number"], submission_time, execution_time)
	else:
		judgement["points"] = "N.A."
	return judgement

def log(team: str, judgement: Dict[str, any]):
	if team not in judgements:
		judgements[team] = {}
	judgements[team][judgement["question_number"]] = judgement
	if judgement["passed"]:
		questions[judgement["question_number"]]["points"][team] = judgement["points"]

def get_judgement(team: str, question_number: int):
	print(judgements.keys())
	if team in judgements and question_number in judgements[team]:
		return judgements[team][question_number]
	else:
		return None