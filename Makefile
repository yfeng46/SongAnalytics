.PHONY: venv download read_data model evaluate database test app clean-tests clean-env clean-pyc

# Below are some other make functions that do useful things

project/bin/activate: requirements.txt
	test -d project || virtualenv project
	. project/bin/activate; pip install -r requirements.txt
	#avcproject/bin/pip install -r requirements.txt
	touch project/bin/activate

venv: project/bin/activate

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

# Run the Flask application
app: app/app.py
	python app/app.py

clean-tests:
	rm -rf test/.pytest_cache
# 	mkdir test/model/test
# 	touch test/model/test/.gitkeep
	
clean-env:
	rm -r project

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache


all: venv download read_data model evaluate database test app clean-tests clean-env clean-pyc
