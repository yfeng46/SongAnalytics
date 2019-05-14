import boto3

s3 = boto3.client('s3')
bucket = s3.Bucket('nw-yifeng')
bucket.download_file('lyrics.csv','music_df.csv','spotify_track_data.csv','topic_dataset.csv','wiki_hot_100s.csv')