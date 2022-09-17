import json
from datetime import datetime

f = open('message_1.json')

data = json.load(f)


for message in data["messages"]:
    try:
        date = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime("%Y-%m-%d %a %H:%M:%S")
        sender = message["sender_name"]
        content = message["content"]
        print(date, sender)
    except KeyError:
        pass


f.close()
