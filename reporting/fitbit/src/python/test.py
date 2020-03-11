import json
import sys
from auth import Auth
from query import Query
from data import Translator
from influx_feeder import InfluxDBFeeder

with open("config.json","r") as f:
	config = json.loads(f.read())

auth = Auth(config['auth'], config['scope'])
query = Query(config['query'], auth)
translator = Translator()
database = InfluxDBFeeder(config['influxdb'])

last_night = query.query('sleep', sys.argv[1])
if last_night != None:
	translated = translator.translate(last_night, "", "")
	print(translated)
	database.write([translated])
else:
	print("Could not load last night")