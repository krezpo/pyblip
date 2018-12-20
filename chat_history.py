# -*- coding: utf-8 -*-

import requests
import json
import yaml
import sys
import pandas as pd

from dateutil import parser

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

excel = {'User': [],
         'Day': [],
         'Hour': [],
         'From': [],
         'To': [],
         'Message': []}


for c in contacts:
    payload['uri'] = "{}/{}?$take={}".format(data['uri'], c, data['messages'])
    r = requests.post(data['url'], headers=headers, data=json.dumps(payload))
    r.encoding = 'utf-8'

    if r.status_code != 200:
        print("IMPOSSIBLE TO GET MESSAGES FOR {}".format(c))
    else:
        try:
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
    
            for i in conversation['items']:
                dt = parser.parse(i['date'])
            
                excel['User'].append(conversation['contact'])
                excel['Day'].append(dt.strftime('%d/%-m/%-y'))
                excel['Hour'].append(dt.strftime('%H:%M:%S.%f')[:-4])
                excel['Message'].append(i['content'])
            
                if i['direction'] == 'sent':
                    excel['From'].append('Bot')
                    excel['To'].append('User')
                else:
                    excel['From'].append('User')
                    excel['To'].append('Bot')

        except Exception as e:
            print("Error: {}".format(e))

df = pd.DataFrame(excel, columns = [*excel])
writer = pd.ExcelWriter('chat_history.xlsx')
df.to_excel(writer, 'history', index=False)
writer.save()
print("Process Finished")
