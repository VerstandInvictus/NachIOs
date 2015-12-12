## IFTTT email to Hook.io Nach step creator.
## This takes a query with parameters of ?sec=<password>&sub=<subject>&bo=<body>&att=<attachmenturl>.
## and adds a step to a preconfigured Nach inbox node with bo as the name and att as a note.
## Subject is currently not implemented but is intended to be used for date/alert/repeat shortcuts.
## It is intended to be used with IFTTT's Maker channel action and Email trigger; in particular,
## attachmenturl implements IFTTT's feature where if you email them an attachment, it becomes a public URL
## hosted on their server to allow a sort of hacky way to (sort of) send arbitrary files to Nach.
## It is not authenticated because IFTTT doesn't really support HTTP auth;
## as a workaround it uses a secret word stored in Hook and fails if that is not a param.
## Not highly secure, but good enough for this application.

import requests

# begin setting vars. This should be your username
user = Hook['env']['nachuser']
# this is set to my inbox's node ID but it could be anything
parentNode = Hook['env']['nachsteproot']
# to avoid publicizing API key, store it in your Hook env vars (hook.io/env).
apiKey = Hook['env']['nachkey']
# ditto - store a secret word or phrase in Hook env vars. This prevents open access to this hook.
magicWord = Hook['env']['magicword']

# now we set the parameters
secret = Hook['params']['sec']
body = Hook['params']['bo']
# sub and at are optional params.
try:
	subject = Hook['params']['sub']
except KeyError:
    subject = None
try:
	note = Hook['params']['at']
except KeyError:
	note = None

# send the request
if magicWord == secret:
	url = 'https://nachapp.com/api/users/' + str(user) + '/nodes'
	r = requests.post(url, auth=(apiKey, ''), verify=False, data= {
	    "parent":parentNode,
	    "name":body
	    })
	print r.text

# <nedry>
else:
	print "Ah ah ah! You didn't say the magic word!"
# </nedry>
