import requests
import json as simplejson

r = requests.get('https://api.appfigures.com/v2/reviews?products=14831371782&count=500&client_key=cadaa98f3bab458a9a321a1505b1e66d', auth=('hello.stanley@yahoo.com', 'stanley123'))

with open('dataTextra', 'w') as outfile:
    outfile.write(simplejson.dumps(simplejson.loads(r.text), indent=4, sort_keys=True))
    outfile.close()
