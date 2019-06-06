import argparse
import boto3
import pandas as pd
import logging
import yaml
import os

logger = logging.getLogger(__name__)

def download_data(url,filename,save_path):
	"""download data from s3 to local
	url(string): 
		preset url to the s3 bucket
	filename(string):
		name of the file or list of the names of the files to download
	save_path(string):
		path of the file(s) to be saved after downloading
	returns: None"""
	if not os.path.exists(save_path):
		os.mkdir(save_path)
	
	if isinstance(filename, list):
		#if filename is a list, downloading multiple files
		for file in filename:
			path = url+file
			logger.info("download the file "+ file)
			df = pd.read_csv(path,sep=',')
			df.to_csv(os.path.join(save_path, file))
			logger.info("save the file to "+save_path+file)

	elif isinstance(filename, str):
		#else, if filename is a single string, download one file
		path = url+filename
		logger.info("download the file "+filename)
		df = pd.read_csv(path,sep=',')
		df.to_csv(os.path.join(save_path, filename))
		logger.info("save the file to "+save_path+filename)
	else:
		#else, raise error
		raise CustomException(filename+" is not a valid file name.")

	return

def run_download_data(args):
	with open(args.config, "r") as f:
		config = yaml.load(f,Loader=yaml.SafeLoader)
		
	config_load = config["project"]['load_data']

	if args.url is None:
		args.url = config_load['url']
	if args.file_key is None:
		args.file_key = config_load['files']
	if args.output_file_path is None:
		args.output_file_path = config_load['folder']
	logger.info("Download data from "+args.url)
	
	download_data(args.url,args.file_key,args.output_file_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Download data from S3")
	# add argument
	parser.add_argument("--config",default="config.yml",help='path to yaml file with configurations')
	parser.add_argument("--url", type=str,help="url of database")
	parser.add_argument("--file_key", type=str,help="Name of the file in S3 that you want to download")
	parser.add_argument("--output_file_path",type=str,help="output directory for downloaded file")
	
	args = parser.parse_args()
	run_download_data(args)

