##get list of matches from all challenger players on a specified server

import requests
import urllib.request
import json
import pandas as pd
import csv
import time


queueid = "420" ##corresponds to ranked, 5v5, soloqueue summoner rift games
millisecondsPerDay = 86400000

def get(key, beginTime=1578470400000, server="na1"):
	endTime = str(beginTime + millisecondsPerDay)
	matchList = set([])
	## to do: abstract away the hard coded file paths
	with open('C:\\Users\\Jay\\Desktop\\LOLstats\\playerinfo.csv') as csv_file:
		csv_reader = csv.reader(csv_file)
		for row in csv_reader:
			##api limit to 1 call every 1.2 seconds. Code takes at least 0.4 seconds to run
			time.sleep(0.8)
			account_id = row[3]
			if account_id != "accountId":
				print(account_id)

				response = requests.get("https://"+server+".api.riotgames.com/lol/match/v4/matchlists/by-account/"+account_id+"?queue="+queueid+"&api_key="+key+"&beginTime="+str(beginTime)+"&endTime="+endTime)
				#response = urllib.request.urlopen("https://"+server+".api.riotgames.com/lol/match/v4/matchlists/by-account/"+account_id+"?queue="+queueid+"&api_key="+key+"&beginTime="+str(beginTime)+"&endTime="+endTime)

				print(response)
				if response.status_code !=200:
					continue

				text = json.dumps(response.json(), sort_keys=True, indent=4)
				matches = json.loads(text)

				for match in matches['matches']:
					matchList.add(match['gameId'])

	return matchList

	

def write(matches, fileName="matchlist.csv"):
	## to do: abstract away the hard coded file paths
	with open('C:\\Users\\Jay\\Desktop\\LOLstats\\'+fileName, "w") as f:
		for match in matches:
			f.write(str(match) +"\n")



