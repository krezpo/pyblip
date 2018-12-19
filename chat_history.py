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
           "uri": data['uri'] + "?$take={}".format(data['threads'])}

r = requests.post(data['url'], headers=headers, data=json.dumps(payload))
r.encoding = 'utf-8'

if r.status_code != 200:
    print("An error has occurred, please verify.")
    print("HTTP STATUS CODE: {}".format(r.status_code))
    sys.exit(-1)
else:

    contacts = [i['identity'] for i in r.json()['resource']['items']]


for c in contacts:
    payload['uri'] = "{}/{}?$take={}".format(data['uri'], c, data['messages'])
    r = requests.post(data['url'], headers=headers, data=json.dumps(payload))
    r.encoding = 'utf-8'

    if r.status_code != 200:
        print("IMPOSSIBLE TO GET MESSAGES FOR {}".format(c))
    else:
        conversation = {}
    
        conversation['contact'] = c
        conversation['total'] = r.json()['resource']['total']
        conversation['items'] = r.json()['resource']['items']

        print("\\\\----------------------------------")
        print(". URL: {}".format(r.url))
        print(". URI: {}".format(payload['uri']))
        print(". HTTP Status Code: {}".format(r.status_code))
        print(". Contact: {}".format(conversation['contact']))
        print(". Total of exchanged messages: {}".format(conversation['total']))
        print("")
    
        print("{}\t{}\t{}\t{}".format("From", "To", "Timestamp", "Message"))
        for i in conversation['items']:
            if i['direction'] == 'sent':
                print("{}\t{}\t{}\t{}".format("Bot", conversation['contact'], i['date'], i['content']))
            else:
                print("{}\t{}\t{}\t{}".format(conversation['contact'], "Bot", i['date'], i['content']))

        print("")

# TO-DO:
    # Save conversations in an excel
