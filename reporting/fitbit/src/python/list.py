import json
import sys
from auth import Auth
from query import Query
from data import Translator
from influx_feeder import InfluxDBFeeder
import json

with open("config.json","r") as f:
	config = json.loads(f.read())

auth = Auth(config['auth'], config['scope'])
query = Query(config['query'], auth)
translator = Translator()
database = InfluxDBFeeder(config['influxdb'])

data = query.list_before('sleep','2018-12-31')
with open("sleep_list.json","w") as f:
	f.write(json.dumps(data))