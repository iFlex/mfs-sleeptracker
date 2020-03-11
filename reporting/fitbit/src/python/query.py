import requests
import json
from datetime import datetime, timedelta

class Query:

	def __init__(self, config, auth_provider):
		self.auth = auth_provider
		self.update_config(config)


	def update_config(self, config):
		self.query_date_endpoint = config['query_date_endpoint']
		self.query_range_endpoint = config['query_range_endpoint']
		self.query_list_endpoint = config['query_list_endpoint']
		self.date_format = config['date_format']


	def query(self, scope_item, date):
		auth_token = self.auth.get_token()
		auth_header = "Bearer %s" % auth_token['access_token']
	
		endpoint = self.query_date_endpoint % (auth_token['user_id'], scope_item, date)

		response = requests.post(endpoint, headers={'Authorization': auth_header})

		if response.status_code == 200:
			return json.loads(response.text)
		else:
			print(response.text)
			
		return None
