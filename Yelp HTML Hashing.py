import collections
import hashlib
from bs4 import BeautifulSoup
from collections import defaultdict
import lxml
import re

with open('yelp.html', 'r', encoding='utf-8') as f:
    yelp_html = f.read().encode(encoding='utf-8')
    checksum = hashlib.md5(yelp_html).hexdigest()
    #assert checksum == "4a74a0ee9cefee773e76a22a52d45a8e", "Downloaded file has incorrect checksum!"

with open('yelp.html', 'r', encoding='utf-8') as yelp_file:
    yelp_html = yelp_file.read()


rankings = collections.defaultdict(dict)

i = 0

soup = BeautifulSoup(yelp_html, "lxml")
restaurants = soup.find_all("li", class_ = "regular-search-result")

for restaurant in restaurants:
    tags1 = restaurant.find("span", class_ = "indexed-biz-name")
    name = tags1.text.strip()[3:]
    rankings[i]["name"] = name.strip()

    tags2 = str(restaurant.find("div", class_="i-stars"))
    stars = re.findall('\d\.\d', tags2)
    rankings[i]["stars"] = stars[0]

    tags3 = restaurant.find("span", class_="review-count rating-qualifier")
    reviews = tags3.text
    num = [s for s in reviews.split() if s.isdigit()]
    num2 = ""
    num3 = num2.join(num)
    rankings[i]["numrevs"] = int(num3)

    tags4 = restaurant.find("span", class_="business-attribute price-range")
    rankings[i]["price"] = tags4.text

    i+=1

print(rankings)


