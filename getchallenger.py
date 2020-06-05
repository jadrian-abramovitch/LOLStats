##builds the list of the top players on each server to observe
import requests
import json
import pandas as pd
import time


def get_list(key, challengerLeagueId = "974b70e3-28eb-3b60-9e9f-82a8efa19f10", server="na1"):
	response = requests.get("https://"+server+".api.riotgames.com/lol/league/v4/leagues/"+challengerLeagueId+"?api_key="+key)
	text = json.dumps(response.json(), sort_keys=True, indent=4)

	summoner_list = []
	data = json.loads(text)["entries"]
	for summoner in data:
		dict1 = {}
		accountresponse = requests.get("https://"+server+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner['summonerName']+"?api_key="+key)
		accountid = json.dumps(accountresponse.json(), sort_keys=True, indent=4)
		player = json.loads(accountid)

		try:
			print(player['id'])
			dict1 = {"Name":summoner['summonerName'], "id":summoner['summonerId'], "accountId":player['accountId']}
			summoner_list.append(dict1)
		except:
			print("no id found")
			
		time.sleep(1.2)

	df = pd.DataFrame(summoner_list) 
	df.to_csv('C:\\Users\\Jay\\Desktop\\LOLstats\\playerinfo.csv')

