import requests
from datetime import datetime
import os
import json
import pytz
from django.views.decorators.csrf import csrf_exempt


api_key = "6a0c0dd6f5fe299a55e79d388afb256f"
file_path = 'weather_app/files/feedback.json'


# Make an API call to a openweathermap.org API using latitude and longitude co-ords
def call_weather(lat, lon):
	if -90.0 <= float(lat) <= 90.0 and -180.0 <= float(lon) <= 180.0:
		# URL to call 'onecall' API to get weather information
		data_url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s" \
		           "&exclude=minute,hourly,alerts&units=metric&appid=%s" % (lat, lon, api_key)

		# URL to call 'weather' API as 'onecall' does not contain name information
		name_url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s' % (lat, lon, api_key)

		resp = requests.get(name_url)
		name_data = json.loads(resp.text)

		# Make the API call and convert the JSON responses to  dict
		response = requests.get(data_url)
		data = json.loads(response.text)

		# Get current date/time and adjust using given timezone
		datetime_converted = datetime.now(pytz.timezone(data['timezone']))
		print(datetime_converted)

		# Build a dict to hold the weather data we want from the API call
		weather_data = {
			'name': name_data['name'],
			'lat': data['lat'],
			'lon': data['lon'],
			'desc': data['current']['weather'][0]['description'].capitalize(),
			'timezone': data['timezone'],
			'time': str(datetime_converted.strftime('%H:%M:%S - %b %d %Y')),
			'curr': data['current']['temp'],
			'feels': data['current']['feels_like'],
			'min': data['daily'][0]['temp']['min'],
			'max': data['daily'][0]['temp']['max'],
			'humidity': data['current']['humidity']
		}

		return weather_data
	else:
		return False


# Retrieve feedback comments, can be changed later to read from database rather than json
# for greater security ie. at the moment the commenter's emails are exposed
def get_feedback():
	feedback = ''
	# Check if the feedback file is not empty, then load the feedback
	if os.path.getsize(file_path) > 0:
		with open(file_path, 'r') as f:
			feedback = json.load(f)

	return feedback


''' For the following function I chose to use JSON from the response.POST rather than 
passing the form class to this function, as json.loads/dumps does a kind of clean on 
the data already, and since I want to save it as JSON then it makes sense to keep it 
in this format, rather than build a JSON dict from scratch element by element. I would 
change this implementation of course if saving to a database and use element.cleaned_data() '''


# Save the feedback comment to json file, can be updated later to write to a database
@csrf_exempt
def save_feedback(json_data):
	# Get current time/date and append to the dict
	curr_time = datetime.now()
	format_time = {'time': curr_time.strftime('%d/%m/%Y %H:%M:%S')}
	json_data.update(format_time)

	del json_data['csrfmiddlewaretoken']

	# Write the json to the comments file
	with open(file_path, 'r+') as f:
		# If the file is empty for some reason, add the array square braces
		if os.path.getsize(file_path) == 0:
			json_init = "[]"
			file_data = json.loads(json_init)
		else:
			file_data = json.load(f)

		# Append the new feedback, then write to file
		file_data.append(json_data)
		new_data = json.dumps(file_data, indent=4)
		f.seek(0)
		csrf_exempt(f.write(new_data))

		# Return the appended JSON to be rendered
		return file_data
