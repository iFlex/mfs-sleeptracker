import json
import sys
import re
from auth import Auth
from query import Query
from fitbit_translator import Translator
from feed import FeedManager
from influx_feeder import InfluxDBFeeder
from datetime import datetime
import traceback


with open("config.json","r") as f:
	config = json.loads(f.read())

auth = Auth(config['auth'])
query = Query(config['query'], auth)
translator = Translator({"user":"Liviu"})
database = InfluxDBFeeder(config['influxdb'])
feed_manager = FeedManager(config['feeds'], query, database, translator)


def is_datetime(dtstring):
	formats = ["%Y-%m-%d", "%Y-%m-%d-%H", "%Y-%m-%d-%H:%M", "%Y-%m-%d-%H:%M:%S"]
	for format in formats:
		try:
			print("Trying to decode '%s' len:%d with %s" %(dtstring, len(dtstring), format))
			return datetime.strptime(dtstring, format)
		except Exception as e:
			pass
	return None


def extract_arguments(args):
	arguments = []
	for arg in args:
		split = arg.split("::")
		
		if len(split) == 1 and feed_manager.has_feed(split[0]):
			arguments.append([split[0]])
		if len(split) == 2:
	   		feed = split[0]
	   		mode_or_date = split[1]
	   		dt = is_datetime(mode_or_date)
	   		print(dt)
	   		if feed_manager.has_feed(feed) and (feed_manager.is_valid_update_mode(mode_or_date) or (not dt == None)):
	   			if dt == None:
	   				arguments.append([feed, mode_or_date])
	   			else:
	   				arguments.append([feed, dt])
	
	return arguments


def update_feeds(arguments):
	if len(arguments) > 0:
		for argument in arguments:
			try:
				if len(argument) == 1:
					feed_manager.update_feed(argument[0])
				if len(argument) == 2:
					if feed_manager.is_valid_update_mode(argument[1]):
						feed_manager.update_feed(argument[0], argument[1])
					else:
						feed_manager.update_feed(argument[0],'custom', argument[1])
			except Exception as e:
				print("Failure")
				traceback.print_exc(file=sys.stdout)
	else:
		feed_manager.update()


arguments = extract_arguments(sys.argv)
update_feeds(arguments)