class Translator:

	def translate(self, data_in, format_in, format_out):
		return {
	        "measurement": "sleep",
	        "tags": {
	            "person": "Liviu"
	        },
	        "time": data_in['sleep'][0]['dateOfSleep'] + "T23:00:00Z",
	        "fields": {
	            "asleep": float(data_in['summary']['totalMinutesAsleep']),
	            "awake": float(data_in['summary']['stages']['wake']),
	            "deep":float(data_in['summary']['stages']['deep']),
	            "light":float(data_in['summary']['stages']['light']),
	            "rem":float(data_in['summary']['stages']['rem'])
	        }
    	}
