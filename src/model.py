
import argparse
import pandas as pd
import logging
import yaml

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import log_loss
from sklearn.ensemble import RandomForestRegressor
from sklearn import ensemble
import pickle


logger = logging.getLogger(__name__)

def model(train_data,filename):
	"""building and saving the model
	train_data:
		dataframe of training data to build the model
	filename:
		pave to save the model
	return: .sav file of the pre-trained model"""
	df = pd.read_csv(train_data,index_col=0)
	logger.info("reading training data from "+train_data)
	df_lyrics_model = df[['title','artist','year_x','lyrics','danceability']]
	df_lyrics_model.dropna()


	params = {'n_estimators': 400, 'max_depth': 4, 'min_samples_split': 3,
          'learning_rate': 0.05, 'loss': 'ls'}

	# define our model
	text_clf = Pipeline(
	    [('vect', TfidfVectorizer()),
	     ('clf', ensemble.GradientBoostingRegressor(**params))])

	# train our model on training data
	text_clf.fit(df_lyrics_model.lyrics.values.astype('U'), df_lyrics_model.danceability)
	# save the model to disk

	pickle.dump(text_clf, open(filename, 'wb'))
	logger.info("Model is saved as "+filename)
	logger.info("Save the model to "+filename)
	return text_clf

def run_model(args):
	"""function to run the model
	args: 
		input when running the model
	"""
	with open(args.config, "r") as f:
		config = yaml.load(f,Loader=yaml.SafeLoader)

	config_read = config["project"]["read_data"]
	config_model = config["project"]["train_model"]
	if args.train_data is None:
		args.train_data = config_read['train']
	if args.save_model is None:
		args.save_model = config_model['model']
	if not args.save_model.endswith('.sav'):
		raise Exception('invalid save path for the model. Has to end with .sav')

	model(args.train_data,args.save_model)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read the csv file")
	# add argument
	parser.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	parser.add_argument("--train_data", type=str,help="path to csv file of training data")
	parser.add_argument("--save_model", type=str, help="path to save the model")

	args = parser.parse_args()

	run_model(args)

