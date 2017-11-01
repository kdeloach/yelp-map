#!/usr/bin/env python
import json
import os
import sys
import time

import requests


TOKEN = os.environ['TOKEN']

MAX_LIMIT = 50
MAX_OFFSET = 1000
SORT_ORDERS = ['best_match', 'rating', 'review_count', 'distance']

search_term = sys.argv[1]

offsets = [i for i in range(0, MAX_OFFSET - MAX_LIMIT + 1, MAX_LIMIT)]

headers = {
    'Authorization': 'Bearer {}'.format(TOKEN),
}

defaults = {
    'location': 'Philadelphia, PA',
    'categories': search_term,
    'radius': 40000,
    'limit': MAX_LIMIT,
}

results = {}

for sort_by in SORT_ORDERS:
    for offset in offsets:
        payload = {}
        payload.update(defaults)
        payload.update({
            'offset': offset,
            'sort_by': sort_by,
        })

        res = requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=headers)
        items = res.json()['businesses']

        sys.stderr.write('{}, {}, {}\n'.format(sort_by, offset, len(items)))

        if not items:
            break

        for item in items:
            id = item['id']
            results[id] = item

        time.sleep(0.2)

json.dump(results, sys.stdout)
