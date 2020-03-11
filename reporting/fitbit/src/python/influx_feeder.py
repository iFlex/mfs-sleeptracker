from influxdb import InfluxDBClient

class InfluxDBFeeder:

	def __init__(self, config):
		self.update_config(config)
		self.client = InfluxDBClient(self.host, self.port, self.user, self.password, self.database)


	def update_config(self, config):
		self.user = config['user']
		self.password = config['password']
		self.database = config['database']
		self.host = config['host']
		self.port = config['port']


	def write(self, data):
		self.client.write_points(data)