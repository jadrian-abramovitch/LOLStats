##This will be the process regulator, responsible for updating the relevant information everyday, and then update the database
import getmatchlist
import getchallenger
import dbInteractor
import time
import os.path
import json
import math
from championTranslator import Champ_Ids, positions
from dbInteractor import dbInteract

class operations():

	def __init__(self, beginTime):
		##get new trial key from https://developer.riotgames.com/ every day
		self.key = "RGAPI-043b5837-2a0b-4601-b3ec-e05b785c0491"
		self.beginTime=beginTime
		self.endTime= int((time.time())*1000) ##current time
		self.msPerDay = 86400000
		self.last_compiled_day = 0

	def generate_json(self):
		full_dict = {}
		tmp = Champ_Ids.getDict()
		print(type(tmp))
		for champ_id, champ_name in Champ_Ids.getDict().items():
			champ_dict = {}

			for position in positions.position_list():
				csdiff = dbInteract.champAverage(champ_id, position)
				champ_dict[position] = csdiff

			full_dict[champ_name] = champ_dict

		json_data = json.dumps(full_dict)
		with open('csdiffs.json', 'w') as outfile:
			json.dump(json_data, outfile)

	def generate_challenger_list(self):
		getchallenger.get_list(self.key)

	def generate_match_lists(self):
		iter = 1
		time = self.beginTime

		while time <= self.endTime:
			if os.path.exists(str(iter) + ".csv"):
				self.last_compiled_day = iter
				continue
			else:
				matches = getmatchlist.get(self.key, beginTime=time)
				getmatchlist.write(matches, fileName=str(iter)+".csv")
			time += self.msPerDay
			iter += 1

	def push_data_to_database(self):
		if not os.path.exists("master.db"):
			print("test")
			dbInteract.initializeDb()

		#for fileNumber in range(self.last_compiled_day + 1, 1000):
		for fileNumber in range(13, 1000):
			if os.path.exists(str(fileNumber)+".csv"):
				print(str(fileNumber)+".csv")
				#try:
				dbInteract.writeDb(str(fileNumber), self.key)
				#except:
				#print("write to dB failed")
			else:
				break

if __name__ == '__main__':
	beginTime=1578470400000 ##corresponds to the beginning of season 10, from the discord
	new_session = operations(beginTime)
	#new_session.generate_challenger_list()
	#new_session.generate_match_lists()
	#new_session.push_data_to_database()
	new_session.generate_json()
