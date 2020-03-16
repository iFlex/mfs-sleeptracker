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


from datetime import datetime, timedelta
import time

forward_step = timedelta(days=1)

start_date = datetime.strptime("2019-10-22","%Y-%m-%d")
end_date = datetime.strptime("2019-12-31","%Y-%m-%d")

while start_date < end_date:
	strdate = start_date.strftime("%Y-%m-%d")
	start_date += forward_step

	print("Fetching data for: %s" % strdate)
	try:
		last_night = query.query('sleep', strdate)
		if last_night != None:
			translated = translator.translate(last_night, "", "")
			print(translated)
			database.write([translated])
		else:
			print("Could not load")
	except Exception as e:
		print(e)
		
	time.sleep(1.0)