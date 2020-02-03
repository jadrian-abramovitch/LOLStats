##need to be careful with the implementation because it will write the same game to the database multiple times
##if i run the script on the same games

import requests
import json
import pandas as pd
import time
import sqlite3

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

				#dict1 = {"matchid":game[0:10], "lane":lane, "Champion":champid, "CSD10":csd10, "CSD20":csd20}
				#masterList.append(dict1)
			time.sleep(0.8)
			#iter+=1
			#print(iter)
			#if iter>=50:
			#	break

	conn.commit()
	conn.close()

#df = pd.DataFrame(masterList) 
#df.to_csv('C:\\Users\\Jay\\Desktop\\LOLstats\\master.csv')
#print(df)



##champ - opposingchamp - csdiff@10 - csdiff@15 - csdiff@20 - role - matchid

##to do next: figure out how to parse json, then find te api that will give me my info, then figure out how to get match id's for pro games
##need to decode champ id number to champion
##maybe use diamond plus games to get enough matchup data? is it safe to assume high level will mimic pro?
##using only pro data will have much less data, but that data will be more accurate