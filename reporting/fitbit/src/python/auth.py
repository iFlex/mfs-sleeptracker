import urllib.parse
import requests
import json
from base64 import b64encode
from datetime import datetime, timedelta

#ToDo: add logger

class Auth:
	
	def __init__(self, config, scope):
		self.update_config(config)
		self.scope = scope
		self.token = None
		self.datetime_format = "%Y-%m-%d-%H:%M:%S"


	def update_config(self, config):
		self.token_location = config['token_location']
		self.token_uri = config['token_uri']
		self.authorise_uri = config['authorise_uri']
		self.client_id = config['client_id']
		self.client_secret = config['client_secret']
		self.auth_code = config['auth_code']
		self.redirect_uri = config['redirect_uri']


	def is_token_valid(self):
		mandatory_keys = ['access_token','valid_until','refresh_token','user_id']
		
		for key in mandatory_keys:
			if key not in self.token:
				return False

		return True


	def calculate_token_expiry_date(self):
		expiry = datetime.now() + timedelta(seconds=self.token['expires_in'])
		self.token['valid_until'] = expiry.strftime(self.datetime_format)


	def seconds_till_token_expiry(self):
		valid_until = datetime.strptime(self.token['valid_until'], self.datetime_format)
		now = datetime.now()
		sign = 1
		if valid_until < now:
			sign = -1
		print("Sign: %d" % sign)
		return sign * (valid_until - now).seconds


	def load_token_from_file(self):
		try:
			f = open(self.token_location, "r")
			self.token = json.loads(f.read())
			
			if self.is_token_valid():
				return None
			return "Token Missing Mandatory Keys"
		except Exception as e:
			return e


	def save_token_to_file(self):
		try:
			self.calculate_token_expiry_date()
			f = open(self.token_location, "w")
			f.write(json.dumps(self.token))
		except Exception as e:
			print("Failure to save token to disk: %s" % str(e))


	def get_auth_header(self):
		return "Basic %s" % b64encode(bytes(self.client_id+":"+self.client_secret,'utf-8')).decode("utf-8")


	def refresh_token(self):
		endpoint = self.token_uri
		auth_header = self.get_auth_header()
		body = {
			'grant_type':'refresh_token',
			'refresh_token':self.token['refresh_token'],
		}
		
		print("Token Refresh")
		print("endpoint:"+str(endpoint))
		try:
			resp = requests.post(endpoint, headers={'Authorization': auth_header}, data=body)
			
			if resp.status_code == 200:
				self.token = json.loads(resp.text)
				self.save_token_to_file()
			else:
				return response.text
		except Exception as e:
			return e



	def request_token(self):
		endpoint = self.token_uri
		auth_header = self.get_auth_header()
		body = {
			'code':self.auth_code,
			'grant_type':'authorization_code',
			'client_id':self.client_id,
			'redirect_uri':self.redirect_uri
		}
		

		print("Token Refresh")
		print("endpoint:"+str(endpoint))
		try:
			resp = requests.post(endpoint, headers={'Authorization': auth_header}, data=body)
			response = json.loads(resp.text)


			if resp.status_code == 200:
				self.token = json.loads(resp.text)
				self.save_token_to_file()
			else:
				return response.text

		except Exception as e:
			return e


	def get_user_auth_grant_url(self):
		params = urllib.parse.urlencode({
			'response_type':'code',	
			'client_id': self.client_id, 
			'redirect_uri': self.redirect_uri, 
			'scope': " ".join(self.scope)
		})
		return "%s?%s" % (self.authorise_uri, params)


	def get_token(self):
		error = self.load_token_from_file()
		if error:
			token_error = self.request_token()
			if token_error != None:
				print("Please authorise this application to obtain a new token by visiting:")
				print(self.get_user_auth_grant_url())
				return None
		else:
			ttl = self.seconds_till_token_expiry()
			print("Time till token expiry: %d" % ttl)
			if ttl <= 0:
				token_refresh_error = self.refresh_token()
		
		return self.token
'''
def query(token, user, date):
	url = 'https://api.fitbit.com/1.2/user/%s/sleep/date/%s.json' % (user,date)
	auth_header = 'Bearer %s' % token
	resp = requests.get(url,headers={'Authorization': auth_header})
	print(resp)
	return resp.text

def query_range(token, user, startd, endd):
	#GET https://api.fitbit.com/1.2/user/[user-id]/sleep/date/[startDate]/[endDate].json
	url = 'https://api.fitbit.com/1.2/user/%s/sleep/date/%s/%s.json' % (user,startd,endd)
	auth_header = 'Bearer %s' % token
	resp = requests.get(url,headers={'Authorization': auth_header})
	print(resp)
	return resp.text
'''