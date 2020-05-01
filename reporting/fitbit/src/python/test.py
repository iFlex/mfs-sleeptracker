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
data = query.query_range('heartrate',datetime(2020,3,13,23,55),datetime(2020,3,14,0,5))
translator = Translator({"user":"Liviu"})

print(translator.translate(data, "heartrate"))