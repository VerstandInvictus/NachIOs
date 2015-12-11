import requests
apikey = Hook['env']['nachkey']
value = Hook['params']['val']
secret = Hook['params']['sec']
magicword = Hook['env']['magicword']

if secret == magicword:
	r= requests.post('https://nachapp.com/api/trackers/1673/measures', 
    	             auth=(apikey, ''), 
        	         verify=False,
            	     data= {"value":value})
	print r.text

else:
	print "Ah ah ah! You didn't say the magic word!"
