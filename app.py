
import datetime, time, math
from flask import Flask, jsonify
import requests


app = Flask(__name__)


# TODO: set a proper app id here
APPID = 0
CITY = 'London,uk'
WEATHER_API = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={appid}'


# for now, allow us to test without an app id
if not APPID:
	APPID = 'b6907d289e10d714a6e88b30761fae22'
	WEATHER_API = 'https://samples.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}'


@app.route('/weather/london/<string:dt>/<string:hour_min>')
@app.route('/weather/london/<string:dt>/<string:hour_min>/<string:metric>')
def weather(dt, hour_min, metric=None):
	# Get the data
	data = requests.get(WEATHER_API.format(appid=APPID, city=CITY))
	data = data.json()

	# Get a timestamp for the datetime specified
	hour, minute = int(hour_min[0:2]), int(hour_min[2:4])
	year, month, day = int(dt[0:4]), int(dt[4:6]), int(dt[6:8])
	try:
		dt = datetime.datetime(year, month, day, hour, minute)
	except ValueError as e:
		return jsonify({"status": "error", "message": "Incorrect date format"})
	timestamp = int(time.mktime(dt.timetuple()))
	day = dt.strftime('%Y-%m-%d %H:%M')

	# Look up data for this timestamp
	data = [x for x in data['list'] if x['dt'] == timestamp]
	if not data:
		return jsonify({"status": "error", "message": "No data for {}".format(day)})
	data = data[0]

	# Format results
	# NOTE: could get celsius directly, since their api accepts "units" (default is K, can be metric (C) or imperial (F))
	result = data['main']
	result['temperature'] = "%sC" % (math.ceil(float(data['main']['temp']) - 273.15))
	result['humidity'] = "%s%%" % result['humidity']
	result['description'] = ", ".join(x['description'] for x in data['weather'])

	if metric:
		if metric not in result:
			result = {"status": "error", "message": "No data for '%s'" % metric}
		else:
			result = {metric: result.get(metric)}

	return jsonify(result)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000)
