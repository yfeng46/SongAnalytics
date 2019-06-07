.PHONY: download read_data model evaluate database test app

# Below are some other make functions that do useful things


# Get data from request
data/lyrics.csv data/spotify_track_data.csv data/wiki_hot_100s.csv: src/download.py
	python run.py download_data --config=config/config.yml
download: data/lyrics.csv data/spotify_track_data.csv data/wiki_hot_100s.csv

#clean the data
data/lyrics_track_train.csv data/lyrics_track_test.csv: src/read_data.py
	python run.py read_data --config=config/config.yml
read_data: data/lyrics_track_train.csv data/lyrics_track_test.csv

# Fit model
models/model.sav: src/model.py
	python run.py model --config=config/config.yml
model: models/model.sav

# Evaluate Model
models/evaluation.txt: src/evaluate.py
	python run.py evaluate --config=config/config.yml
evaluate: models/evaluation.txt

#build the database
song_analytics.db: src/tables.py
	python run.py database --flag=false
database: song_analytics.db

#unitest
test: venv
	pytest

app: app/app.py
	python app/app.py


all: download read_data model evaluate database test app
