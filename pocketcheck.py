import pocket
import config
import time
import pymongo
import requests
import json


def updateTimeDb():
    timedb.insert_one(dict(
        _id="lastTime",
        lastTime=time.time()
    ))


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

# initialize the connection to Mongo
client = pymongo.MongoClient()
db = client.nachios
timedb = db.time

# when did we last check for new articles?
lastTime = timedb.find_one({"_id": "lastTime"})['lastTime']

p = pocket.Pocket(config.consumerKey, config.accessToken)

# get all archived articles modified since last check
articleList = p.get(detailType="simple", state="archive", since=lastTime)

# this goes through the raw Pocket data for each item and finds a nonblank
# string to use as a title. The IFTTT -> Hook version of this was failing
# I think because sometimes the only usable title is resolved_url and
# IFTTT sends a blank title in such cases.

# also IFTTT is really slow compared to running this on a 30 second cron.
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

# set last checked time to now
updateTimeDb()
