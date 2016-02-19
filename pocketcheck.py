import pocket
import config
import time
import pymongo

client = pymongo.MongoClient()
db = client.nachios
timedb = db.time

# this code for init-ing blank DB
# timedb.insert_one(dict(
#     _id="lastTime",
#     lastTime=time.time()
# ))

lastTime = timedb.find_one({"_id": "lastTime"})['lastTime']

p = pocket.Pocket(config.consumerKey, config.accessToken)

articleList = p.get(detailType="simple", state="archive", since=lastTime)

for each in articleList[0]['list'].itervalues():
    buildup = ' '
    for title in(
            each['resolved_title'],
            each['given_title'],
            each['resolved_url']):
        if len(title) == 0:
            pass
        else:
            print title
            break
