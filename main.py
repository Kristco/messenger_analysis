import pandas as pd
import re
from datetime import datetime
import json

def decoder(string):
  patterns = {
    r'\u00c4\u0085': 'ą',
    r'\u00c4\u008d': 'č',
    r'\u00c4\u0099': 'ę',
    r'\u00c4\u0097': 'ė',
    r'\u00c4\u00af': 'į',
    r'\u00c5\u00a1': 'š',
    r'\u00c5\u00b3': 'ų',
    r'\u00c5\u00ab': 'ū',
    r'\u00c5\u00be': 'ž',
  }
  for pattern, replacement in patterns.items():
      string = re.sub(pattern, replacement, string)
  return string

def json_df(data):
    messages_list = data['messages']

    df = pd.DataFrame(messages_list)
    df.rename(columns={'timestamp_ms': 'time', 'sender_name': 'name'}, inplace=True)
    df['content'].fillna('', inplace=True)
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime("%Y-%m-%d %a %H:%M:%S"))
    df['time'] = pd.to_datetime(df['time'])

    df['name'] = df['name'].apply(lambda x: decoder(x))
    df['content'] = df['content'].apply(lambda x: decoder(x))
    return df

with open('message_1.json') as json_file:
    data = json.load(json_file)

df = json_df(data)

df_you = df[df['name'] == 'Your name']
df_other = df[df['name'] == 'Other name']

msgr = pd.DataFrame({'name': [df_other['name'][0]], 'sent': [len(df_other)], 'got': [len(df_you)]})
msgr = msgr.set_index('name')

print(msgr)