import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.model_selection import train_test_split

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.read_data import clean_data
from src.model import model

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def test_split():
	"""unitest for the clean_data function"""
	lyrics = "test/lyrics_test.csv"
	tracks = "test/spotify_track_data_test.csv"
	billboard = "test/wiki_hot_100s_test.csv"
	df_lyrics = pd.read_csv(lyrics,index_col=0)
	df_tracks = pd.read_csv(tracks,index_col=0)
	df_hot = pd.read_csv(billboard,index_col=0)

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

	test_train,test_test = train_test_split(df_lyrics_track,test_size=0.3,random_state=123)
	(result_train,result_test) = clean_data(lyrics,tracks,billboard)
	# result_train = result[0]
	# result_test = result[1]
	test_train.reset_index(drop=True,inplace=True)
	test_test.reset_index(drop=True,inplace=True)
	result_train.reset_index(drop=True,inplace=True)
	result_test.reset_index(drop=True,inplace=True)
	assert (test_train.equals(result_train)) and (test_test.equals(result_test))

def model():
	"""Testing the model that the return result should be within 0 and 1"""
	lyrics = "Quando sono solo Sogno all'orizzonte E mancan le parole Sì lo so che non c'è luce In una stanza quando manca il sole Se non ci sei tu con me, con me"
	test_model = model("lyrics_trac_train_test.xlsx","test_model.sav")
	dance = test_model.predict([lyrics])
	assert (dance>=0) and (dance<=1)



