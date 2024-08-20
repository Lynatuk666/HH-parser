import json
import pprint

with open("data.json", "r") as file:
    data_json = file.read()

data = json.loads(data_json)

pprint.pprint(data)