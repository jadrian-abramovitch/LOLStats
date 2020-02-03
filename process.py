import getmatchlist
import getchallenger
import dbInteractor
import time
import os.path

key = "RGAPI-ba8eacd5-3e10-4942-92cb-ded93ceb447d"
beginTime=1578470400000
endTime= int((time.time())*1000)
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
