import argparse
import boto3
import pandas as pd
import logging

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
	
	if isinstance(filename, list):
		#if filename is a list, downloading multiple files
		for file in filename:
			path = url+filename
			logger.info("download file from "+path)
			df = pd.read_csv(path,sep=',')
			df.to_csv(save_path+file)
			logger.info("save the file to "+save_path+file)

	elif isinstance(filename, str):
		#else, if filename is a single string, download one file
		path = url+filename
		logger.info("download file from "+path)
		df = pd.read_csv(path,sep=',')
		df.to_csv(save_path+file)
		logger.info("save the file to "+save_path+file)
	else:
		#else, raise error
		raise CustomException(filename+" is not a valid file name.")

	return


if __name__ == "__main__":
	url = 'https://s3-us-west-2.amazonaws.com/nu-yifeng/'
	parser = argparse.ArgumentParser(description="Download data from S3")
	# add argument
	parser.add_argument("file_key", default = ["lyrics.csv","spotify_track_data.csv","wiki_hot_100s.csv"],type=str,help="Name of the file in S3 that you want to download")
	parser.add_argument("output_file_path", default = "../data/",type=str,help="output directory for downloaded file")
	args = parser.parse_args()
	download_data(url,args.file_key, args.output_file_path)