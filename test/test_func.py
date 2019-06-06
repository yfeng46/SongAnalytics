import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.tables import prediction


def test_database():
	# Initialize the Flask application
	app = Flask(__name__)

	# Configure flask app from config.py
	app.config.from_object('config')

	# Initialize the database
	db = SQLAlchemy(app)

	result = db.session.query(prediction).get(1)
	assert (result.user_input,result.danceability) == ("Quando sono solo Sogno all'orizzonte E mancan le parole Sì lo so che non c'è luce In una stanza quando manca il sole Se non ci sei tu con me, con me",0.05)
