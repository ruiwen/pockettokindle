#!/home/ruiwen/projects/pockettokindle/venv/bin/python

import json
import requests

from readability import ReaderClient

import config


# Obtain 'since' from somewhere
try:
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
        since = metadata.get('since') or config.ORIGIN_SINCE

except FileNotFoundError as e:
    since = config.ORIGIN_SINCE

res = requests.get('https://getpocket.com/v3/get/', json={
        "consumer_key": config.POCKET_CONSUMER_KEY,
        "access_token": config.POCKET_ACCESS_KEY,
        "tag": "kindle",
        "since": since,
        "sort": "oldest",
        "count": 20
       })


articles = res.json()['list']

if not articles:
    since = res.json()['since']
    with open('metadata.json', 'w') as f:
        f.write(json.dumps({"since": since}))
    exit(0)

articles = sorted(articles.values(), key=lambda x: x['sort_id'])  # sort_id is provided by pocket to denote sort order

since = str(int(articles[-1]['time_updated']) + 1)
with open('metadata.json', 'w') as f:
    f.write(json.dumps({"since": since}))

readability = ReaderClient(
                token_key=config.READABILITY_USER_KEY,
                token_secret=config.READABILITY_USER_SECRET,
                consumer_key=config.READABILITY_CONSUMER_KEY,
                consumer_secret=config.READABILITY_CONSUMER_SECRET
              )

for a in articles:
    readability.add_bookmark(a['resolved_url'])

