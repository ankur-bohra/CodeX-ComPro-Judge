import json
import difflib
from Tio import Tio

questions = []
participants = []
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
			question_data["multiplier"] = info["multipliers"][level]
			question_data["submissions"] = {}
			with open(f"questions/{question_name}/QUESTION.md", "r") as file:
				question_data["question"] = file.read()
			with open(f"questions/{question_name}/INPUT.txt", "r") as file:
				question_data["input"] = file.read()
			with open(f"questions/{question_name}/ANSWER.txt", "r") as file:
				question_data["answer"] = file.read()
			questions.append(question_data)

def get_leaderboard(include_times=True):
	'''Sorts the participants by their submissions.'''
	global questions
	total_time = {user_id: 0 for user_id in participants}
	slowest_times = {}
	for user_id in participants:
		for question in questions:
			submissions = question["submissions"]
			if user_id in submissions:
				total_time[user_id] += submissions[user_id]
			else:
				if question["number"] not in slowest_times:
					slowest_times[question["number"]] = min( list(submissions.values()) + [0])  # Add 0 in case no one submitted
				total_time[user_id] += slowest_times[question["number"]] * question["multiplier"]

	# Flatten and sort
	total_time = [{"id": user_id, "time": total_time[user_id]} for user_id in total_time]
	total_time.sort(key=lambda p_data: p_data["time"])  # Sort by total time
	if not include_times:
		total_time = [p_data["id"] for p_data in total_time]  # Get the participant ids
	return total_time 

class Diff:
	def __init__(self, correct, wrong):
		correct_lines, wrong_lines = correct.split("\n"), wrong.split("\n")
		self.unified = difflib.unified_diff(
			a=[line + "\n" for line in correct_lines], b=[line + "\n" for line in wrong_lines],
			fromfile="Answer", tofile="Output"
		)
		self.unified = "".join(self.unified)  # unified_diff gives lines, each with the \n added
		import sys
		sys.stdout.writelines(self.unified)

		sequence = difflib.SequenceMatcher(None, correct_lines, wrong_lines)
		first_correct_lines = sequence.get_matching_blocks()[0].size
		self.flod = first_correct_lines + 1
		pass

class Judgement:
	def __init__(self, question, response):
		self.output = response.stdout
		self.passed = self.output.strip() == question["answer"].strip()
		self.question = question
		self.time_taken = float(response.real_time)
		self.diff = Diff(question["answer"], self.output)

site = Tio()
def judge(question_number: int, language: str, source_code: str) -> Judgement:
	question = questions[question_number]
	request = site.new_request(language, source_code, question["input"])
	response = site.send(request)
	judgement = Judgement(question, response)
	return judgement

def log(user_id: int, judgement: Judgement):
	if user_id not in participants:
		participants.append(user_id)
		judgements[user_id] = {}
	judgements[user_id][judgement.question["number"]] = judgement
	if judgement.passed:
		questions[judgement.question["number"]]["submissions"][user_id] = judgement.time_taken

def get_judgement(user_id: int, question_number: int):
	if user_id in judgements and question_number in judgements[user_id]:
		return judgements[user_id][question_number]
	else:
		return None