import boto3

s3 = boto3.resource("s3")
bucket = s3.Bucket('nw-yifeng')
bucket.download_file('lyrics.csv','spotify_track_data.csv','wiki_hot_100s.csv')