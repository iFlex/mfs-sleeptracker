import requests
import json
from datetime import datetime, timedelta

class Query:

	def __init__(self, config, auth_provider):
		self.auth = auth_provider
		self.update_config(config)


	def update_config(self, config):
		self.config = config
		self.date_format = config['date_format']


	def get_token(self):
		return self.auth.get_token()


	def get_auth_header(self, auth_token):
		return "Bearer %s" % auth_token['access_token']


	def return_query_result(self, response):
		print("Datasource Response: %s " % response)
		if response.status_code == 200:
			print("Raw data length %sB" % len(response.text))
			#print(response.text)
			return json.loads(response.text)
		else:
			print(response.text)
			
		return None


	def lookup_parameters(self, parameters, local_context):
		result = []
		for par in parameters:
			if par in local_context:
				result.append(local_context[par])
			elif par in local_context['auth_token']:
				result.append(local_context['auth_token'][par])
			else:
				result.append(None)

		print("URL parameters")
		print(result)
		return result


	def parametrise_endpoint(self, endpoint, parameters, local_context):
		return endpoint.format(*self.lookup_parameters(parameters, local_context))
		

	def get_endpoint(self, feed_name, endpoint_type, local_context):
		if feed_name in self.config:
			url = self.config[feed_name][endpoint_type]
			return (self.parametrise_endpoint(url, self.config[feed_name]['parameters'], local_context), self.config[feed_name]['method'])

		return (self.parametrise_endpoint(self.query_date_endpoint, self.config['parameters'], local_context), self.config['method'])


	def query(self, scope_item, sd, ed=None):
		if scope_item in self.config:
			if 'range_endpoint' in self.config[scope_item]:
				return self.query_range(scope_item, sd, ed)
			else:
				if ed != None:
					print("warning: Feed '%s' does not support range queries, attempting a single date query using start_date %s" % (scope_item, sd))
				return self.query_date(scope_item, sd)
		else:
			raise Exception("Unknown feed '%s'" % scope_item)


	def query_date(self, scope_item, date):
		auth_token = self.get_token()
		endpoint, method = self.get_endpoint(scope_item, 'date_endpoint', {
			"feed_name":scope_item, 
			"date":date.date(), 
			"auth_token":auth_token
		}) #self.query_date_endpoint % (auth_token['user_id'], scope_item, date.date()) 
		print("Date Query")
		print(endpoint)

		if method == 'POST':
			r = requests.post(endpoint, headers={'Authorization': self.get_auth_header(auth_token)})
		elif method == 'GET':
			r = requests.get(endpoint, headers={'Authorization': self.get_auth_header(auth_token)})
		
		return self.return_query_result(r)
		

	def query_range(self, scope_item, start_date, end_date):	
		auth_token = self.get_token()
		time_fromat = "%H:%M"
		endpoint, method = self.get_endpoint(scope_item, 'range_endpoint', {
			"feed_name":scope_item,
			"start_datetime":start_date,
			"end_datetime":end_date, 
			"start_date":start_date.date(), 
			"end_date":end_date.date(),
			"auth_token":auth_token,
			"start_time":start_date.strftime(time_fromat),
			"end_time":end_date.strftime(time_fromat)
		})

		print("Range Query")
		print(endpoint)
		
		if   method == 'POST':
			r = requests.post(endpoint, headers={'Authorization': self.get_auth_header(auth_token)})
		elif method == 'GET':
			r = requests.get(endpoint, headers={'Authorization': self.get_auth_header(auth_token)})
		return self.return_query_result(r)


	def get_all_pages(self, endpoint):
		result =  []
		has_more_pages = True
		while has_more_pages == True:
			r = self.return_query_result(requests.post(endpoint, headers={'Authorization': self.get_auth_header()}))
			if r == None or ('pagination' not in r or 'next' not in r['pagination'] or len(r['pagination']['next']) < 1):
				has_more_pages = False
			else:
				endpoint = r['pagination']['next']
				print("Next page: %s" % endpoint)
			
			result.append(r['sleep'])
		
		return result


	def list_before(self, scope_item, date):
		endpoint = self.query_list_endpoint % (scope_item)
		endpoint += "?beforeDate=%s&offset=0&limit=100&sort=desc" % (date)
		print(endpoint)
		return self.get_all_pages(endpoint)
		

	def list_after(self, scope_item, date):
		endpoint = self.query_list_endpoint % (scope_item)
		endpoint += "?afterDate=%s&offset=0&limit=100&sort=asc" % (date)
		print(endpoint)
		return self.get_all_pages(endpoint)
