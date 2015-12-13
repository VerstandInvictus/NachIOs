# IFTTT email to Hook.io Nach step creator.
#
# Parameters are:
# ?sec=<password>
# &par=<parentNode>
# &msg=_B_R_K_{{Subject}}_B_R_K_{{Body}}_B_R_K_{{AttachmentUrl}}
#
# The MSG parameter can contain as many items as needed and they'll all
# be added as notes.
# 
# It is done in this strange way because IFTTT doesn't escape URLs within
# its URLs.
#
# This adds a step to a preconfigured Nach inbox node with sub as the name
# and att and body as a note if present.
#
# It is intended to be used with IFTTT's Maker channel action and
# Email trigger; in particular, attachmenturl implements IFTTT's feature
# where if you email them an attachment, it becomes a public URL hosted on
# their server to allow a sort of hacky way to send arbitrary files to Nach.
#
# The killer app here is using this with a shortcut Intent on android
# via something like Email to Me so that you can share anything to Nach
# with two taps.
#
# It is not authenticated because IFTTT doesn't really support HTTP auth;
# as a workaround it uses a secret word stored in Hook
# and fails if that is not a param.
#
# Not highly secure, but good enough for this application.

import requests
import json
import urllib

# begin setting vars. This should be your username
user = Hook['env']['nachuser']
# default value - this is set to my inbox's node ID but it could be anything
parentNode = Hook['env']['nachsteproot']
# to avoid publicizing API key, store it in your Hook env vars (hook.io/env).
apiKey = Hook['env']['nachkey']
# ditto - store a secret word or phrase in Hook env vars.
# This prevents open access to this hook.
magicWord = Hook['env']['magicword']

# now we set the parameters
secret = Hook['params']['sec']
# catch empty params
try:
    parentNode = Hook['params']['par']
except KeyError:
    pass

msgstring = urllib.unquote(str(Hook['req']['url'])).split("_B_R_K_")

subject = msgstring[1]
if len(msgstring) > 2:
    notes = msgstring[2:]

# I use the below signature to keep Gmail on Android from prompting me
# about empty body in an email. This could be anything you want. Strip it out:

newNotes = list()
signature = "\n\n______\n"
for each in notes:
	if each.endswith(signature):
		cut = len(signature)
		each = each[:-cut]
	newNotes.append(each)
notes = newNotes

#strip blank params passed from IFTT/placeholders
toss = ("", '\n', "NOSUB")
filteredNotes = [x for x in notes if not x in toss]
notes=filteredNotes

# if no subject (read: shared from Google Keep), use body as subject
# but keep body as note in case of errors/truncation
if subject in toss:
    subject = notes[0]

# DRY note posting func
def postNote(node, content, apikey):
    url = 'https://nachapp.com/api/nodes/' + str(node) + "/notes"
    newNote = requests.post(url, auth=(apikey, ''), verify=False, data={
        "content" : content
    })
    return newNote

# make the step
if magicWord == secret:
    url = 'https://nachapp.com/api/users/' + str(user) + '/nodes'
    newStep = requests.post(url, auth=(apiKey, ''), verify=False, data={
        "parent": parentNode,
        "type": "Step",
        "name": subject
    })
    # get the ID of the new step and add notes
    response = json.loads(newStep.text)
    nodeId = response['id']
    for each in notes:
        bodyNote = postNote(nodeId, each, apiKey)

# nedry.py
# unfortunately Hook doesn't let python access logs yet
else:
    print "Ah ah ah! You didn't say the magic word!"
