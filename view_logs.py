import pickle
import pprint
import glob

with open("LOGS/08_42.dat", "rb") as log:
	data = pickle.load(log)
	for team in data:
		for q_no in data[team]:
			data[team][q_no]["code"] = "<code>"
			data[team][q_no]["output"] = "<output>"
	pprint.pprint(data)