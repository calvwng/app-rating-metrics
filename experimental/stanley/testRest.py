import requests

r = requests.get('https://api.appfigures.com/v2/products/search/snapchat?client_key=cadaa98f3bab458a9a321a1505b1e66d', auth=('hello.stanley@yahoo.com', 'stanley123'))

r.status_code

print(r.text)
