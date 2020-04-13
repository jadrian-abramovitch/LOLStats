##This will be the process regulator, responsible for updating the relevant information everyday, and then update the database
import getmatchlist
import getchallenger
import dbInteractor
import time
import os.path
##get new trial key from https://developer.riotgames.com/ every day
key = ""
beginTime=1578470400000 ##corresponds to the beginning of season 10, from the discord
endTime= int((time.time())*1000) ##current time
msPerDay = 86400000

getchallenger.get(key)

iter = 1
time = beginTime
while time <= endTime:
	matches = getmatchlist.get(key, beginTime=time)
	getmatchlist.write(matches, fileName=str(iter)+".csv")
	time += msPerDay
	iter +=1

for fileNumber in range(1, 1000):
	if not os.path.exists("master.db"):
		dbInteractor.initializeDb()

	print(str(fileNumber)+".csv")
	
	if os.path.exists(str(fileNumber)+".csv"):
		print("hello")
		try:
			dbInteractor.writeDb(str(fileNumber), key)
		except:
			print("write to dB failed")
	else:
		break
