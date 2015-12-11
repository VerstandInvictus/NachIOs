## Hook.io Nach tracker updater.
## This takes a query with parameters of ?val=<number>&tr=<Nach tracker ID>&sec=<secret word>
## and adds a data point to the Nach tracker with ID corresponding to the "tr" param.
## It is intended to be used with IFTTT's Maker channel action but could be triggered from anywhere.
## It is not authenticated because IFTTT doesn't really support HTTP auth;
## as a workaround it uses a secret word stored in Hook and fails if that is not a param.
## Not highly secure, but good enough for this application.

import requests
# to avoid publicizing API key, store it in your Hook env vars (hook.io/env).
apikey = Hook['env']['nachkey']
value = Hook['params']['val']
secret = Hook['params']['sec']
tracker = Hook['params']['tr']
# ditto - store a secret word or phrase in Hook env vars. This prevents open access to this hook.
magicword = Hook['env']['magicword']

# send the request
if secret == magicword:
	url = 'https://nachapp.com/api/trackers/' + str(tracker) + '/measures'
	r= requests.post(url, auth=(apikey, ''), verify=False, data= {"value":value})
	print r.text

# <nedry>
else:
	print "Ah ah ah! You didn't say the magic word!"
# </nedry>
