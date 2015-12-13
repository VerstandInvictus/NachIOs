import requests
import json

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


# make the step
if magicWord == secret:
    'https://nachapp.com/api/users/' + str(user) + '/nodes'
    listNodes = requests.get(url, auth=apiKey, ''), verify=False

# nedry.py
# unfortunately Hook doesn't let python access logs yet
else:
    print "Ah ah ah! You didn't say the magic word!"
