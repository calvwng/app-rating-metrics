import json as simplejson
import requests

EMAIL = 'hello.stanley@yahoo.com'
PASSWORD = 'stanley123'
PRODUCT_ID = '14831371782'
CLIENT_KEY = 'cadaa98f3bab458a9a321a1505b1e66d'

fileName = raw_input("Enter name of output file for reviews: ")

initialReq = requests.get('https://api.appfigures.com/v2/reviews?products={0}&count=500&client_key={1}'.format(PRODUCT_ID, CLIENT_KEY), auth=(EMAIL, PASSWORD))

values = simplejson.loads(initialReq.text)
numPages = values['pages']
reviews = values['reviews']

for currentPage in range(2, numPages + 1):
    reqStr = 'https://api.appfigures.com/v2/reviews?products={0}&count=500&page={1}&client_key={2}'.format(PRODUCT_ID, str(currentPage), CLIENT_KEY)
    r = requests.get(reqStr, auth=(EMAIL, PASSWORD))
    reviews += simplejson.loads(r.text)['reviews']
    
with open(fileName, 'w') as outfile:
    outfile.write(simplejson.dumps(reviews, indent=4, sort_keys=True))
    outfile.close()

