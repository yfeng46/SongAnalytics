"""Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.
To understand different arguments, run `python run.py --help`
"""
import argparse
import logging.config
from app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("churn-predictor")
logger.debug('Test log')

from src.download import run_download_data
from src.read_data import run_clean_data
from src.model import run_model
from src.tables import create
from src.evaluate import run_evaluate


def run_app(args):
	"""run the all the functions"""
	app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Run components of the model source code")
	subparsers = parser.add_subparsers()

	# download data subparser
	sub_download = subparsers.add_parser("download_data",description="Download data from S3")
	sub_download.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	sub_download.add_argument("--url", type=str,help="url of database")
	sub_download.add_argument("--file_key", type=str,help="Name of the file in S3 that you want to download")
	sub_download.add_argument("--output_file_path",type=str,help="output directory for downloaded file")
	sub_download.set_defaults(func=run_download_data)

	# read/clean data subparser
	sub_read = subparsers.add_parser("read_data",description="Read the csv file")
	# add argument
	sub_read.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	sub_read.add_argument("--lyrics", type=str,help="path to csv file of lyrics data")
	sub_read.add_argument("--tracks", type=str,help="path to csv file of tracks data")
	sub_read.add_argument("--billboard",type=str,help="path to csv file of billboard data")
	sub_read.add_argument("--save_train",type=str,help="path to save the training data")
	sub_read.add_argument("--save_test",type=str,help="path to save the testing data")
	sub_read.set_defaults(func=run_clean_data)

	# build model subparser
	sub_model = subparsers.add_parser("model", description="Build the model")
	# add argument
	sub_model.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	sub_model.add_argument("--train_data", type=str,help="path to csv file of training data")
	sub_model.add_argument("--save_model", type=str, help="path to save the model")
	sub_model.set_defaults(func=run_model)


	# evaluate the model
	sub_evaluate = subparsers.add_parser("evaluate", description="Evaluate the model performance")
	sub_evaluate.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	sub_evaluate.add_argument("--model", type=str,help="path to the model")
	sub_evaluate.add_argument("--train", type=str,help="path to the training data")
	sub_evaluate.add_argument("--test",type=str, help="path to the testing data")
	sub_evaluate.add_argument("--save_path", type=str, help="path to save the model evaluation")
	sub_evaluate.set_defaults(func=run_evaluate)

	# create database
	sub_database = subparsers.add_parser("database", description="Create the database")
	sub_database.add_argument("--flag",default=True,help='to build the database in RDS or local')
	sub_database.set_defaults(func=create)
	
	# RUN APP subparser
	sb_run = subparsers.add_parser("app", description="Run Flask app")
	sb_run.set_defaults(func=run_app)

	args = parser.parse_args()
	args.func(args)



