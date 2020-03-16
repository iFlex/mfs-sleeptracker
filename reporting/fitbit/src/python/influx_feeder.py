from influxdb import InfluxDBClient
from datetime import datetime

import traceback
import sys

class InfluxDBFeeder:

	def __init__(self, config):
		self.update_config(config)
		self.client = InfluxDBClient(self.host, self.port, self.user, self.password, self.database)
		self.time_format = "%Y-%m-%dT%H:%M:%SZ" 

	def update_config(self, config):
		self.user = config['user']
		self.password = config['password']
		self.database = config['database']
		self.host = config['host']
		self.port = config['port']


	def write(self, data):
		self.client.write_points(data)


	def extract_first_timestamp(self, data):
		return data['series'][0]['values'][0][0]


	#ToDo: prevent sql injection by clensing arguments
	def get_last_timestamp(self, measurement, user):
		#clean up database and measurement or use prepared queries
		try:
			rs = self.client.query("select * from %s where person = '%s' order by time desc limit 1" % (measurement, user));
			timestamp = self.extract_first_timestamp(rs.raw)
			return datetime.strptime(timestamp, self.time_format)
		except Exception as e:
			print("Failed to retrieve last written record for %s" % measurement)
			traceback.print_exc(file=sys.stdout)
			return None