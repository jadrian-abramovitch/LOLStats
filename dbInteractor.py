##responsible for taking info about the challenger games played each day, getting the info for each match and writing to the master database

import requests
import json
import pandas as pd
import time
import sqlite3

class dbInteract():

	def initializeDb():
		conn = sqlite3.connect('master.db')
		c = conn.cursor()
		c.execute("""CREATE TABLE master (
			matchid text,
			lane text,
			champion text,
			csd10 text,
			csd20 text
			)""")
		conn.commit()
		conn.close()

	def writeDb(fileName, key, server="na1"):
		iter = 0
		conn = sqlite3.connect('master.db')
		c = conn.cursor()
		masterList = []
		with open('C:\\Users\\Jay\\Desktop\\LOLstats\\'+fileName+'.csv', "r") as f:
			for game in f:
				##need to splice because there is a blank space at the end
				response = requests.get("https://"+server+".api.riotgames.com/lol/match/v4/matches/"+game[0:10]+"?api_key="+key)
				print(response.status_code)
				if response.status_code !=200:
					continue

				text = json.dumps(response.json(), sort_keys=True, indent=4)
				data = json.loads(text)["participants"]

				for participants in data:
					try:
						lane = participants['timeline']['lane']
					except:
						lane = ""
					try:
						champid = participants['championId']
					except:
						champid = ""
					try:
						csd10 = participants['timeline']['csDiffPerMinDeltas']['0-10']
					except:
						csd10 = ""
					try:
						csd20 = participants['timeline']['csDiffPerMinDeltas']['10-20']
					except:
						csd20 = ""

					c.execute("INSERT INTO master(matchid, lane, champion, csd10, csd20) VALUES (?, ?, ?, ?, ?)", (game[0:10], lane, champid, csd10, csd20))

				##api limit is 1 call every 1.2 seconds, code takes at least 0.4 seconds to run
				time.sleep(0.8)


		conn.commit()
		conn.close()

	def champAverage(champ, position):
		conn = sqlite3.connect('master.db')
		c = conn.cursor()
		c.execute("SELECT csd10 FROM master WHERE champion=\'{}\' AND lane=\'{}\'".format(str(champ), position))
		csList = c.fetchall()
		num = 0
		total = 0
		for csDiff in csList:
			num +=1
			if csDiff[0]:
				total += float(csDiff[0])
		if num < 5:
			return None
		average = total/num
		print(average)
		return average

