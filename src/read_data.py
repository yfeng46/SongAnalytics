
import argparse
import boto3
import pandas as pd
import logging
import yaml
import os
import sklearn
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

def read_data(lyrics,tracks,billboard):
	"""Read the file for the project
	lyrics(string): 
		csv for the lyrics data
	tracks(string):
		csv for the tracks data
	billboard(string):
		csv for the billboard data
	returns: list of pandas dataframe"""

	df_lyrics = pd.read_csv(lyrics,index_col=0)
	logger.info("Read lyrics data from "+lyrics)
	df_tracks = pd.read_csv(tracks,index_col=0)
	logger.info("Read tracks data from "+tracks)
	df_hot = pd.read_csv(billboard,index_col=0)
	logger.info("Read billboard data from "+billboard)


	return [df_lyrics,df_tracks,df_hot]

def clean_data(lyrics,tracks,billboard):
	"""clean the data and merge the data for future modeling
	df_lyrics:
		dataframe that contains lyrics data
	df_tracks:
		dataframe that contains tracks information
	df_hot:
		dataframe that contains billboard ranking information
	returns: training and testing dataframe"""
	
	dfs = read_data(lyrics,tracks,billboard)
	df_lyrics = dfs[0]
	df_tracks = dfs[1]
	df_hot = dfs[2]

	#clean the tie string in ranking
	tieIndex = df_hot.index[df_hot['no']=='Tie'].tolist()
	for index in tieIndex:
		value = df_hot.no[index-1]
		df_hot.loc[index,'no'] = value
	#define rank variable that change the no variable to a binary response
	df_hot['rank'] = df_hot['no'].apply(lambda x: 1 if int(x)<=10 else 0 )
	#define popularity variable that change the no to a continuous variable
	df_hot['popularity'] = df_hot['no'].apply(lambda x: 100*(1/int(x)))

	#Remove the meaningless words from the lyrics data
	df_lyrics['lyrics'] = df_lyrics['lyrics'].replace({"\n": " "}, regex=True)
	# Another Pre-preprocessing step: Removal of '-' from the CourseId field
	#['oh','ha','aa','na','um','yeah','la']
	df_lyrics['lyrics'] = df_lyrics['lyrics'].replace({"oh": " ","ha":" ","aa":" ","na":" ","um":" ","yeah":" ","la":" ","chorus":" "}, regex=True)

	###define the join key for all dataframes so they can be merged together

	#df_hot
	df_hot["clean_title"] = df_hot["title"].map(lambda x: x.strip().lower())
	df_hot['clean_artist'] = df_hot['artist'].map(lambda x: x.strip().lower())
	df_hot['join_key'] = df_hot.apply(lambda row: row.clean_artist[:4]+str(row.year) + row.clean_title[:4], axis=1)

	#df_lyrics
	df_lyrics['clean_artist'] = df_lyrics['artist'].map(lambda x: x.strip().lower())
	df_lyrics['clean_title'] = df_lyrics['title'].map(lambda x: x.strip().lower())
	df_lyrics['join_key'] = df_lyrics.apply(lambda row: row.clean_artist[:4]+str(row.year) + row.clean_title[:4], axis=1)

	#df_tracks
	df_tracks['clean_artist'] = df_tracks['artist_name'].map(lambda x: x.strip().lower())
	df_tracks['clean_title'] = df_tracks['track_name'].map(lambda x: x.strip().lower())
	df_tracks['join_key'] = df_tracks.apply(lambda row: row.clean_artist[:4]+str(row.year) + row.clean_title[:4], axis=1)

	###Merge lyrics and tracks data for the modeling
	df_lyrics_track = pd.merge(df_lyrics, df_tracks, left_on='join_key', right_on='join_key', how='inner')
	df_lyrics_track.dropna()

	df_lyrics_train, df_lyrics_test = train_test_split(df_lyrics_track,test_size=0.3,random_state=123)

	return (df_lyrics_train,df_lyrics_test)

def run_clean_data(args):
	with open(args.config, "r") as f:
		config = yaml.load(f,Loader=yaml.SafeLoader)
		
	config_read = config["project"]['read_data']

	if args.lyrics is None:
		args.lyrics = config_read['lyrics']
	if args.tracks is None:
		args.tracks = config_read['tracks']
	if args.billboard is None:
		args.billboard = config_read['billboard']
	if args.save_train is None:
		args.save_train = config_read['train']
	if args.save_test is None:
		args.save_test = config_read['test']
	results = clean_data(args.lyrics,args.tracks,args.billboard)

	#write the train data
	results[0].to_csv(args.save_train)
	logger.info("output training data is in "+args.save_train)

	#write the test data
	results[1].to_csv(args.save_test)
	logger.info("output testing data is in "+args.save_test)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read the csv file")
	# add argument
	parser.add_argument("--config",default="config/config.yml",help='path to yaml file with configurations')
	parser.add_argument("--lyrics", type=str,help="path to csv file of lyrics data")
	parser.add_argument("--tracks", type=str,help="path to csv file of tracks data")
	parser.add_argument("--billboard",type=str,help="path to csv file of billboard data")
	parser.add_argument("--save_train",type=str,help="path to save the train file")
	parser.add_argument("--save_test",type=str,help="path to save the test data")
	
	args = parser.parse_args()

	run_clean_data(args)
