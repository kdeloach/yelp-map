#!/usr/bin/env python
import json
import sys

fpath = sys.argv[1]

features = []
data = json.load(open(fpath, 'r'))

for key, props in data.iteritems():
    geom = {
        'type': 'Point',
        'coordinates': [
            props['coordinates']['longitude'],
            props['coordinates']['latitude'],
        ],
    }
    features.append({
        'type': 'Feature',
        'properties': {
            'name': props['name'],
        },
        'geometry': geom,
    })

fcoll = {
    'type': 'FeatureCollection',
    'features': features,
}

json.dump(fcoll, sys.stdout)
