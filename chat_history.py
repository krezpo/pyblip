# -*- coding: utf-8 -*-

import requests
import json
import yaml
import sys

with open("config.yml", 'r') as stream:
    try:
        data = yaml.load(stream)
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit(-1)

headers = {"Content-Type": "application/json",
           "Authorization": data['key']}

payload = {"id": data['id'],
           "method": "get",
           "uri": "/threads"}

r = requests.post(data['url'], headers=headers, data=json.dumps(payload))
r.encoding = 'utf-8'

if r.status_code != 200:
    print("An error has occurred, please verify.")
    print("HTTP STATUS CODE: {}".format(r.status_code))
else:
    print("{}".format(r.text))

# TO-DO:
    # Format Threads
    # Get the conversations for each user
    # Format conversations
    # Save conversations
