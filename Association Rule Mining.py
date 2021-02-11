import re
from collections import defaultdict
from itertools import combinations

def normalize_string(s):
    assert type (s) is str
    strip1 = re.compile('([^\s\w]|_)+')
    strip2 = strip1.sub('', s)
    return strip2.lower()

def get_normalized_words (s):
    assert type(s) is str
    norm_text = normalize_string(s)
    split1 = norm_text.split()
    return split1

def make_itemsets(words):
    list2 = []
    for word in words:
        group = set()
        for w in word:
            group.add(w)
        list2.append(group)

    return list2

def update_pair_counts(pair_counts, itemset):
    assert type(pair_counts) is defaultdict
    pairs = (combinations(itemset, 2))
    for pair in pairs:
        pair_counts[pair] += 1
        pair_counts[pair[::-1]] += 1

    return pair_counts

def update_item_counts(item_counts, itemset):
    for item in itemset:
        item_counts[item] += 1
    return

def filter_rules_by_conf(pair_counts, item_counts, threshold):
    rules = {}  # (item_a, item_b) -> conf (item_a => item_b)
    for pair in pair_counts:
        p = pair_counts[pair]
        c = p / item_counts[pair[0]]
        if c >= threshold:
            rules[pair] = c

    return rules

def find_assoc_rules(receipts, threshold):
    pair_counts = defaultdict(int)
    item_counts = defaultdict(int)
    for r in receipts:
        update_pair_counts(pair_counts, r)
        update_item_counts(item_counts, r)
    t = filter_rules_by_conf(pair_counts, item_counts, threshold)
    return t


def on_vocareum():
    import os
    return os.path.exists('.voc')


def download(file, local_dir="", url_base=None, checksum=None):
    import os, requests, hashlib, io
    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(file))


if on_vocareum():
    DATA_PATH = "./resource/asnlib/publicdata/"
else:
    DATA_PATH = ""
datasets = {'groceries.csv': '0a3d21c692be5c8ce55c93e59543dcbe'}

for filename, checksum in datasets.items():
    download(filename, local_dir=DATA_PATH, checksum=checksum)

with open('{}{}'.format(DATA_PATH, 'groceries.csv')) as fp:
    groceries_file = fp.read()
print(groceries_file[0:250] + "...\n... (etc.) ...")  # Prints the first 250 characters only
print("\n(All data appears to be ready.)")

# Confidence threshold
THRESHOLD = 0.5

# Only consider rules for items appearing at least `MIN_COUNT` times.
MIN_COUNT = 10

gf = groceries_file
gf = gf.splitlines()
basket2 = []

for line in gf:
    basket = line.split(",")
    basket2.append(set(basket))

pair_counts = defaultdict(int)
item_counts = defaultdict(int)

for b in basket2:
    update_pair_counts(pair_counts, b)
    update_item_counts(item_counts, b)

basket_rules = dict()

for (a, b) in pair_counts:
    basket_conf = pair_counts[(a,b)] / item_counts[a]
    if basket_conf >= THRESHOLD and item_counts[a] >= MIN_COUNT:
        basket_rules[(a,b)] = basket_conf

print(basket_rules)