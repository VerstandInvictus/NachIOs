import pocket
import config
import time
import pymongo
import requests
import json
import unidecode
import arrow
requests.packages.urllib3.disable_warnings()


# initialize the connection to Mongo
client = pymongo.MongoClient()
db = client.nachios
timedb = db.time


def updateTimeDb(rtime):
    timedb.drop()
    timedb.insert_one(dict(
        _id="lastTime",
        lastTime=time.time()
    ))
    print "{0}: time updated.".format(rtime)


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

# when did we last check for new articles?
lastTime = timedb.find_one({"_id": "lastTime"})['lastTime']
readableTime = arrow.utcnow().to(
    'US/Pacific').format("YYYY-MM-DD HH:mm:ss ZZ")

# initialize pocket
p = pocket.Pocket(config.consumerKey, config.accessToken)

# get all archived articles modified since last check
articleList = p.get(detailType="simple", state="archive", since=lastTime)

# this goes through the raw Pocket data for each item and finds a nonblank
# string to use as a title. The IFTTT -> Hook version of this was failing
# I think because sometimes the only usable title is resolved_url and
# IFTTT sends a blank title in such cases.

# also IFTTT is really slow compared to running this on a 5 minute cron.
try:
    for each in articleList[0]['list'].itervalues():
        ert = None
        egt = None
        eru = None
        try:
            ert = each['resolved_title']
            egt = each['given_title']
            eru = each['resolved_url'] # not Iluvatar
        except:
            print "{0}: unknown title: {1}".format(
                readableTime,
                each
            )
        for title in(ert, egt, eru, "unknown title"):
            if not title:
                pass
            elif len(title) == 0:
                pass
            else:
                makeStep(title)
                print "{1}: made step for {0}".format(
                    unidecode.unidecode(title),
                    readableTime)
                break
except AttributeError:
    print "{0}: no articles found".format(readableTime)

# set last checked time to now

updateTimeDb(readableTime)
