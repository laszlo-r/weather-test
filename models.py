
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True, nullable=False)
	apicode = db.Column(db.String(32), unique=True, nullable=False)
	weather = db.relationship('WeatherData', backref='location')

class WeatherData(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=False)
	datetime = db.Column(db.DateTime, nullable=False)
	temperature = db.Column(db.Float, nullable=False)
	pressure = db.Column(db.Float, nullable=False)
	humidity = db.Column(db.Float, nullable=False)
	description = db.Column(db.String(100), nullable=True)
