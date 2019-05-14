import boto3

s3 = boto3.client("s3")
s3.download_file("mw-yifeng",'lyrics.csv','spotify_track_data.csv','wiki_hot_100s.csv')