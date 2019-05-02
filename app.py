
import datetime, time, math
from flask import Flask, jsonify, redirect, url_for
import requests
import models


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = models.db
db.init_app(app)
db.create_all(app=app)


# Init db with some test data -- should live in fixtures
with app.app_context():
	if not models.Location.query.count():
		db.session.add(models.Location(name='london', apicode='London,uk'))
		db.session.commit()


# openweathermap api settings -- TODO: set a proper app id here
APPID = 0
WEATHER_API = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={appid}'
# for now, allow us to test without an app id
if not APPID:
	APPID = 'b6907d289e10d714a6e88b30761fae22'
	WEATHER_API = 'https://samples.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}'


def json_error(text):
	return jsonify({"status": "error", "message": text})


@app.route('/')
def main():
	return redirect(url_for('weather'))

@app.route('/weather/')
@app.route('/weather/<string:location>/<string:dt>/<string:hour_min>')
@app.route('/weather/<string:location>/<string:dt>/<string:hour_min>/<string:metric>')
def weather(location=None, dt=None, hour_min=None, metric=None):
	if not dt or not hour_min:
		return json_error("Please specify city and date: /weather/<city>/19700101/0101[/temperature]")

	res = models.Location.query.filter_by(name=location.lower()).first()
	if not res:
		return json_error("Unknown location '%s'" % location)
	location = res

	# Get the datetime specified
	hour, minute = int(hour_min[0:2]), int(hour_min[2:4])
	year, month, day = int(dt[0:4]), int(dt[4:6]), int(dt[6:8])
	try:
		dt = datetime.datetime(year, month, day, hour, minute)
	except ValueError as e:
		return json_error("Incorrect date format, expecting /YYYYMMDD/HHSS")

	# Look for the specific timestamp, only query the api if we don't have it
	weather = models.WeatherData.query.filter_by(location=location, datetime=dt).first()

	# Since using a database, makes sense to cache a good chunk (if not all) of the queried data,
	# with some restrictions to avoid spamming the api (like limiting rate with a timestamp)
	if not weather:
		data = requests.get(WEATHER_API.format(appid=APPID, city=location.apicode)).json()

		def transform(values):
			return models.WeatherData(
				datetime=datetime.datetime.fromtimestamp(values['dt']),
				temperature=math.ceil(float(values['main']['temp']) - 273.15),
				humidity=values['main']['humidity'],
				pressure=values['main']['pressure'],
				description=", ".join(x['description'] for x in values['weather'])
			)

		for values in data['list']:
			location.weather.append(transform(values))
		db.session.commit()

		# Check again, in the new data
		weather = models.WeatherData.query.filter_by(location=location, datetime=dt).first()

	if not weather:
		return json_error("No data for '%s'" % dt.strftime('%Y-%m-%d %H:%M'))

	result = {
		'temperature': "%sC" % weather.temperature,
		'humidity': "%s%%" % weather.humidity,
		'pressure': weather.pressure,
		'description': weather.description
	}

	if metric:
		if metric not in result:
			return json_error("No data for '%s'" % metric)
		result = {metric: result.get(metric)}

	return jsonify(result)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000)
