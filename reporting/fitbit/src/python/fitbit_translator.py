
class Translator:
	
	def __init__(self, config):
		self.translators = {}
		self.translators['sleep'] = self.translate_sleep_record
		self.translators['weight'] = self.translate_weight_record
		self.translators['heartrate'] = self.translate_heartrate_record

		self.update_config(config)


	def update_config(self, config):
		self.user = config['user']


	def get_user(self):
		return self.user


	def translate(self, data, feed_name):
		try:
			translator = self.translators[feed_name]
			return translator(data)
		except Exception as e:
			print("Translation Error")
			print(e)	
		return []


	def translate_sleep_record(self, data):
		return [{
	        "measurement": "sleep",
	        "tags": {
	            "person": self.user
	        },
	        "time": data['sleep'][0]['dateOfSleep'] + "T23:00:00Z",
	        "fields": {
	            "asleep": float(data['summary']['totalMinutesAsleep']),
	            "awake": float(data['summary']['stages']['wake']),
	            "deep":float(data['summary']['stages']['deep']),
	            "light":float(data['summary']['stages']['light']),
	            "rem":float(data['summary']['stages']['rem'])
	        }
    	}]


	def translate_weight_record(self, data):
		result = []
		measurements = data['weight']

		for measurement in measurements:
			result.append({
	        "measurement": "weight",
	        "tags": {
	            "person": self.user,
	            "source": measurement['source']
	        },
	        "time": measurement['date'] + "T" + measurement['time'] + "Z",
	        "fields": {
	            "weight": float(measurement['weight']),
	            "fat": float(measurement.get('fat', 0)),
	        }
    	})

		return result


	def translate_heartrate_record(self, data):
		result = []
		date = data['activities-heart'][0]['dateTime']
		measurements = data['activities-heart-intraday']['dataset']
		
		for measurement in measurements:
			result.append({
	        "measurement": "heartrate",
	        "tags": {
	            "person": self.user
	        },
	        "time": date + "T" + measurement['time'] + "Z",
	        "fields": {
	            "value": float(measurement['value']),
	        }
    	})
		
		return result
