import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
html = urllib.request.urlopen(url)
data = html.read().decode()
sum = 0

try :
    info = json.loads(data)
except:
    info = None

for item in info['comments']:
    comment = item['count']
    sum += int(comment)
    
print(sum)
