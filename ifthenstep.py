# IFTTT email to Hook.io Nach step creator.
#
# Parameters are ?sec=<password>&sub=<subject>&bo=<body>&att=<attachmenturl>.
#
# This adds a step to a preconfigured Nach inbox node with sub as the name
# and att and body as a note if present.
#
# It is intended to be used with IFTTT's Maker channel action and
# Email trigger; in particular, attachmenturl implements IFTTT's feature
# where if you email them an attachment, it becomes a public URL hosted on
# their server to allow a sort of hacky way to send arbitrary files to Nach.
#
# It is not authenticated because IFTTT doesn't really support HTTP auth;
# as a workaround it uses a secret word stored in Hook
# and fails if that is not a param.
#
# Not highly secure, but good enough for this application.

import requests
import json

# begin setting vars. This should be your username
user = Hook['env']['nachuser']
# this is set to my inbox's node ID but it could be anything
parentNode = Hook['env']['nachsteproot']
# to avoid publicizing API key, store it in your Hook env vars (hook.io/env).
apiKey = Hook['env']['nachkey']
# ditto - store a secret word or phrase in Hook env vars.
# This prevents open access to this hook.
magicWord = Hook['env']['magicword']

# now we set the parameters
secret = Hook['params']['sec']
subject = Hook['params']['sub']
# bo and at are optional params; catch cases where they don't exist.
try:
    body = Hook['params']['bo']
except KeyError:
    body = None
try:
    note = Hook['params']['at']
except KeyError:
    note = None

toss = ("", '\n',)

if note in toss:
    note = None
if body in toss:
    note = None
if len(body) < 3:
    body = None
# I use the below signature to keep Gmail on android from prompting me
# about empty body in an email. Strip it out:
signature = "\n\n______\n"
if body.endswith(signature):
    cut = len(signature)
    body = body[:-cut]
    
def postNote(node, content, apikey):
    url = 'https://nachapp.com/api/nodes/' + str(node) + "/notes"
    newNote = requests.post(url, auth=(apikey, ''), verify=False, data={
        "content" : content
    })
    return newNote

# send the request
if magicWord == secret:
    url = 'https://nachapp.com/api/users/' + str(user) + '/nodes'
    newStep = requests.post(url, auth=(apiKey, ''), verify=False, data={
        "parent": parentNode,
        "type": "Step",
        "name": subject
    })
    print newStep.text
    response = json.loads(newStep.text)
    nodeId = response['id']
    if note is not None:
        attNote = postNote(nodeId, note, apiKey)
    if body is not None:
        bodyNote = postNote(nodeId, body, apiKey)

# nedry.py
else:
    print "Ah ah ah! You didn't say the magic word!"
