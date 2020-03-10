import json
from auth import Auth

with open("config.json","r") as f:
	config = json.loads(f.read())

auth = Auth(config['auth'], config['scope'])
token = auth.get_token();
print(token)