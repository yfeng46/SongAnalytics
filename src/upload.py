import boto3

s3 = boto3.client('s3')

s3.upload_file('nw-yifeng','lyrics.csv','music_df.csv','spotify_track_data.csv','topic_dataset.csv','wiki_hot_100s.csv')