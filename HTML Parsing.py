from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL - ')
repetitions = int(input('Enter number of repetitions - '))
position = int(input('Enter link position - '))

#number of repetitions
for i in range(repetitions):
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a')
    count = 0
    for tag in tags:
        count = count+1

#stop at position
        if count>position:
            break
        else:
            url = tag.get('href', None)
            name = tag.contents[0]
print(name)
