# IFTTT email to Hook.io Nach step creator.
#
# Parameters are:
# ?sec=<password> (secret word you set in Hook)
# &par=<parentNode> (Nach node ID)
# &st=<status> (completed, failed, or null)
# &msg=_B_R_K_{{Subject}}_B_R_K_{{Body}}_B_R_K_{{AttachmentUrl}}
#
# The MSG parameter can contain as many items as needed and they'll all
# be added as notes provided they are separated by _B_R_K_. This is
# accomplished by parsing the URL IFTTT requests directly, not via the param.
# 
# It is done in this strange way because IFTTT doesn't escape URLs within
# its URLs. This causes Hook's params to break on restricted chars (read: &).
#
# This adds a step to a preconfigured Nach inbox node with the first nonblank
# BRK param as the subject and all others as notes.
#
# It is intended to be used with IFTTT's Maker channel action and
# Email trigger; in particular, with IFTTT's feature
# where if you email them an attachment, it becomes a public URL hosted on
# their server to allow a sort of hacky way to send arbitrary files to Nach.
#
# The killer app here is using this with a shortcut Intent on android
# via something like Email to Me so that you can share anything to Nach
# with two taps. I also use it for Pocket -> IFTTT -> Hook -> Nach.
#
# It is not authenticated because IFTTT doesn't really support HTTP auth;
# as a workaround it uses a secret word stored in Hook
# and fails if that is not a param.
#
# Not highly secure, but good enough for this application.

import requests
import json
import urllib
import time

# begin setting vars. This should be your username

user = Hook['env']['nachuser']
# to avoid publicizing API key, store it in your Hook env vars (hook.io/env).
apiKey = Hook['env']['nachkey']
# ditto - store a secret word or phrase in Hook env vars.
# This prevents open access to this hook.
magicWord = Hook['env']['magicword']

# now we set the parameters
status = Hook['params']['st']
secret = Hook['params']['sec']
debugParent = 51020

# catch empty params
try:
    parentNode = Hook['params']['par']
except KeyError:
    # default value - this is set to my inbox's node ID but it could be
    # anything
    parentNode = Hook['env']['nachsteproot']


# DRY note posting func
def postNote(node, content, apikey):
    nurl = 'https://nachapp.com/api/nodes/' + str(node) + "/notes"
    newNote = requests.post(nurl, auth=(apikey, ''), verify=False, data={
        "content": content
    })
    return newNote


def debugNote(content):
    global apiKey
    postNote(debugParent, content, apiKey)

# this is where we get the URL and split it to a list of pseudo-params

msg = urllib.unquote(str(Hook['req']['url'].encode('ascii', 'ignore')))
debugNote(msg)
msgstring = msg.split("_B_R_K_")

notes = None
subject = msgstring[1]
if len(msgstring) > 2:
    notes = msgstring[2:]

# I use a signature comprised only of newlines and underscores to keep Gmail
# on Android from prompting me about empty body in an email. Strip it out:
newNotes = list()
if notes:
    for each in notes:
        each = each.strip()
        each = each.rstrip("\n_")
        newNotes.append(each)
notes = newNotes

# strip blank params passed from IFTT/placeholders
toss = ("", '\n', "NOSUB", ' ', '  ')
filteredNotes = [x for x in notes if x not in toss]
notes = filteredNotes
# if no subject (read: shared from Google Keep), use body as subject
# but keep body as note in case of errors/truncation
if subject in toss:
    subject = notes[0]

# custom categorization shortcuts for some of my goals
# replace or delete these with yours
if int(parentNode) == int(Hook['env']['nachsteproot']):
    if any(x in subject.lower() for x in ["music", "song"]):
        parentNode = 47745
    elif any(x in subject.lower() for x in ["deviantart", ]):
        parentNode = 47688
    elif any(x in subject.lower() for x in ["wp", ]):
        parentNode = 49021
    elif any(x in subject.lower() for x in ["[dot]", "ffinit", "fa:"]):
        parentNode = 47739
    elif any(x in subject.lower() for x in ["buy", "amazon", "purchase"]):
        parentNode = 47577
    elif any(x in subject.lower() for x in ["movie", "watch", "show"]):
        parentNode = 47553
    elif any(x in subject.lower() for x in ["book", "calibre", ]):
        parentNode = 47555
    elif any(x in subject.lower() for x in ["pay", "bill"]):
        parentNode = 47557
    elif any(x in subject.lower() for x in ["work", "gus", "teardown"]):
        parentNode = 47541

# make the step
if magicWord == secret:
    url = 'https://nachapp.com/api/users/' + str(user) + '/nodes'
    newStep = requests.post(url, auth=(apiKey, ''), verify=False, data={
        "parent": parentNode,
        "type": "Step",
        "name": subject,
        "status": status
    })

    # get the ID of the new step and add notes
    response = json.loads(newStep.text)
    nodeId = response['id']
    for each in notes:
        bodyNote = postNote(nodeId, each, apiKey)
    # pause - completion doesn't work if we do not do this
    time.sleep(5)
    if status == "completed":
        url = 'https://nachapp.com/api/todos/' + str(nodeId)
        newCompletion = requests.patch(url, auth=(apiKey, ''), verify=False,
                                       data=
                                       {"status": "completed"})

# nedry.py
# unfortunately Hook doesn't let python access logs yet
else:
    print "Ah ah ah! You didn't say the magic word!"
