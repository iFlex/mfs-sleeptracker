from datetime import datetime, timedelta


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

	#Got to account for the fact that fitbit's endpoint just passes midnight and the time field just resets
	def translate_heartrate_record(self, data):
		print(data)
		result = []

		date_format = "%Y-%m-%d"
		pass_midnight = timedelta(days=1)
		date = datetime.strptime(data['activities-heart'][0]['dateTime'], date_format)
		strdate = date.strftime(date_format)
		previous_hour = None
		current_houry = None

		#assuming measurements are in chronological order (cuz otherwise... the endpoint is broken)
		measurements = data['activities-heart-intraday']['dataset']
		for measurement in measurements:
			#assuming time is always HH:mm
			current_hour = int(measurement['time'].split(":")[0])
			if previous_hour != None and current_hour < previous_hour:
				#midnight passed
				date += pass_midnight
				strdate = date.strftime(date_format)
			previous_hour = current_hour
			
			result.append({
		        "measurement": "heartrate",
		        "tags": {
		            "person": self.user
		        },
		        "time": strdate + "T" + measurement['time'] + "Z",
		        "fields": {
		            "value": float(measurement['value']),
		        }
    		})

		return result
