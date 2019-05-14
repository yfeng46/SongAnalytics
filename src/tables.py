import os
import sys

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config
from helpers import create_connection, get_session
import argparse

class lyrics(Base):
    """ Defines the data model for the table `tweet`. """

    __tablename__ = 'lyrics'

    lyrics_id = Column(String(100),primary_key = True, unique=True,nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    year = Column(String(10), unique=False, nullable=False)
    lyrics = Column(Text, unique=False, nullable=True)

    def __repr__(self):
        lyrics_repr = "<lyrics(lyrics_id='%s', title='%s', artist='%s', year='%s',message='%s')>"
        return lyrics_repr % (self.lyrics_id, self.title, self.artist, self.year,self.lyrics)


# ADD CLASS FOR TWEET SCORE TABLE HERE
class wiki_hot_100s(Base):
    """ Define a tweet_score table that has two fields, tweet_id and score"""
    
    __tablename__ = 'wiki_hot_100s'

    hot_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    year = Column(String(10), unique=False, nullable=False)

    def __repr__(self):
        wiki_hot_100s_repr = "<wiki_hot_100s(hot_id='%s', rank='%s', title='%s', artist='%s',year='%s')>"
        return tweet_repr % (self.hot_id, self.rank,self.title,self.artist,self.year)

class tracks(Base):
    """ Defines the data model for the table `tweet`. """

    __tablename__ = 'tracks'

    track_id = Column(String(100),primary_key = True, unique=True,nullable=False)
    year = Column(String(10), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    explicit = Column(Boolean,unique=False,nullable=True)
    track_name = Column(String(100),unique=False,nullable=True)
    track_2nd_id = Column(String(100),unique=False,nullable=False)
    danceability = Column(Float,unique=False,nullable=False)
    energy = Column(Float,unique=False,nullable=False)
    key = Column(Integer,unique=False,nullable=False)
    loudness = Column(Float,unique=False,nullable=False)
    mode = Column(Integer,unique=False,nullable=False)
    speechiness = Column(Float,unique=False,nullable=False)
    acousticness = Column(Float,unique=False,nullable=False)
    instrumentalness = Column(Float,unique=False,nullable=False)
    liveness = Column(Float,unique=False,nullable=False)
    valence = Column(Float,unique=False,nullable=False)
    tempo = Column(Float,unique=False,nullable=False)
    track_type = Column(String(100),unique=False,nullable=True)
    url = Column(String(150),unique=False,nullable=True)
    track_herf = Column(String(150),unique=False,nullable=True)
    analysis_url = Column(String(150),unique=False,nullable=True)
    duration_ms = Column(Integer,unique=False,nullable=True)
    time_signature = Column(Integer,unique=False,nullable=True)

    def __repr__(self):
        lyrics_repr = "<tracks(track_id='%s', year='%s', artist='%s', explicit='%s',track_name='%s',track_2nd_id='%s',danceability='%s',energy='%s',key=='%s',loudness='%s',mode='%s',speechiness='%s',acousticness='%s',instrumentalness='%s',liveness='%s',valence='%s',tempo='%s',track_type='%s',url='%s',track_herf='%s',analysis_url='%s',duration_ms='%s',time_signature='%s'>"
        return lyrics_repr % (self.track_id, self.year, self.artist, self.explicit,self.track_name,self.track_2nd_id,self.danceability,self.energy,self.key,self.loudness,self.mode,self.speechiness,self.acousticness,self.instrumentalness,self.liveness,self.valence,self.tempo,self.track_type,self.url,self.track_herf,self.analysis_url,self.duration_ms,self.time_signature)

class topic(Base):
    """ Defines the data model for the table `tweet`. """

    __tablename__ = 't'

    track_id = Column(String(100),primary_key = True, unique=True,nullable=False)
    year = Column(String(10), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    explicit = Column(Boolean,unique=False,nullable=True)
    track_name = Column(String(100),unique=False,nullable=True)
    track_2nd_id = Column(String(100),unique=False,nullable=False)
    danceability = Column(Float,unique=False,nullable=False)
    energy = Column(Float,unique=False,nullable=False)
    key = Column(Integer,unique=False,nullable=False)
    loudness = Column(Float,unique=False,nullable=False)
    mode = Column(Integer,unique=False,nullable=False)
    speechiness = Column(Float,unique=False,nullable=False)
    acousticness = Column(Float,unique=False,nullable=False)
    instrumentalness = Column(Float,unique=False,nullable=False)
    liveness = Column(Float,unique=False,nullable=False)
    valence = Column(Float,unique=False,nullable=False)
    tempo = Column(Float,unique=False,nullable=False)
    track_type = Column(String(100),unique=False,nullable=True)
    url = Column(String(150),unique=False,nullable=True)
    track_herf = Column(String(150),unique=False,nullable=True)
    analysis_url = Column(String(150),unique=False,nullable=True)
    duration_ms = Column(Integer,unique=False,nullable=True)
    time_signature = Column(Integer,unique=False,nullable=True)

    def __repr__(self):
        lyrics_repr = "<tracks(track_id='%s', year='%s', artist='%s', explicit='%s',track_name='%s',track_2nd_id='%s',danceability='%s',energy='%s',key=='%s',loudness='%s',mode='%s',speechiness='%s',acousticness='%s',instrumentalness='%s',liveness='%s',valence='%s',tempo='%s',track_type='%s',url='%s',track_herf='%s',analysis_url='%s',duration_ms='%s',time_signature='%s'>"
        return lyrics_repr % (self.track_id, self.year, self.artist, self.explicit,self.track_name,self.track_2nd_id,self.danceability,self.energy,self.key,self.loudness,self.mode,self.speechiness,self.acousticness,self.instrumentalness,self.liveness,self.valence,self.tempo,self.track_type,self.url,self.track_herf,self.analysis_url,self.duration_ms,self.time_signature)