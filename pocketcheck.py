import pocket
import config
import time
import pymongo
import requests
import json


def makeStep(titleString):
    url = 'https://nachapp.com/api/users/' + str(config.nachUser) + '/nodes'
    newStep = requests.post(url,
                            auth=(config.nachApiKey, ''),
                            verify=False,
                            data={
                                  "parent": config.nachPTRNode,
                                  "type": "Step",
                                  "name": titleString
                            })
    # pause - completion doesn't work if we do not do this
    response = json.loads(newStep.text)
    nodeId = response['id']
    time.sleep(8)
    url = 'https://nachapp.com/api/todos/' + str(nodeId)
    newCompletion = requests.patch(url,
                                   auth=(config.nachApiKey, ''),
                                   verify=False,
                                   data={"status": "completed"})

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
            makeStep(title)
            break
