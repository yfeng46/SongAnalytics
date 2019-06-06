from sklearn.metrics import mean_squared_error, r2_score
import pickle
import logging
import pandas as pd
import yaml

logger = logging.getLogger(__name__)


def evaluate(model,train,test,save_path):
	"""Evaluate the model performance
	model:
		pretrained model from the model.py file
	train:
		path to training dataframe
	test:
		path to testing dataframe
	save_path:
		path to save the output of the model evaluation
	return: none. Model evaluation is written out as a file."""
	loaded_model = pickle.load(open(model, 'rb'))
	df_train = pd.read_csv(train,index_col=0)
	df_test = pd.read_csv(test,index_col=0)

	# score our model on testing data
	predictions = loaded_model.predict(df_test.lyrics.values.astype('U'))
	mse = mean_squared_error(df_test.danceability, predictions)
	r2 = r2_score(df_train.danceability,loaded_model.predict(df_train.lyrics.values.astype('U')))
	r2_test = r2_score(df_test.danceability,loaded_model.predict(df_test.lyrics.values.astype('U')))

	with open(save_path, 'w') as file:
		file.write("R square: %.4f" % r2)
		file.write("\n")
		file.write("MSE: %.4f" % mse)
		file.write("\n")
		file.write("Test R square: %.4f" % r2_test)
	logger.info("Model performance evaluation is saved to "+save_path)


def run_evaluate(args):
	"""Run the model evaluation function
	args:
		input when running the py file"""
	with open(args.config, "r") as f:
		config = yaml.load(f,Loader=yaml.SafeLoader)

	config_post = config["project"]["post_process"]
	config_read = config["project"]["read_data"]

	if args.model is None:
		args.model = config_post['input_model']
	if args.train is None:
		args.train = config_read['train']
	if args.test is None:
		args.test = config_read['test']
	if args.save_path is None:
		args.save_path = config_post['output']
	evaluate(args.model,args.train,args.test,args.save_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read the csv file")
	# add argument
	parser.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	parser.add_argument("--model", type=str,help="path to the model")
	parser.add_argument("--train", type=str,help="path to the training data")
	parser.add_argument("--test",type=str, help="path to the testing data")
	parser.add_argument("--save_path", type=str, help="path to save the model evaluation")

	args = parser.parse_args()

	run_model(args)