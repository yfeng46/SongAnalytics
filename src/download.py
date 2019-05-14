import argparse
import boto3

# s3 = boto3.client("s3")

# def download_data(args):
#     s3.download_file(args.bucket_name, args.file_key, args.output_file_path)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Download data from S3")

#     # add argument
#     parser.add_argument("--file_key", help="Name of the file in S3 that you want to download")
#     parser.add_argument("--bucket_name", help="s3 bucket name")
#     parser.add_argument("--output_file_path", help="output path for downloaded file")

#     args = parser.parse_args()

# s3 = boto3.client("s3")
# s3.download_file("mw-yifeng",'lyrics.csv','spotify_track_data.csv','wiki_hot_100s.csv')

import pandas as pd


def download_data(url,filename,save_path):
	path = url+filename
	print(path)
    df = pd.read_csv(path,sep=',')
    df.to_csv(save_path)



if __name__ == "__main__":
    url = 'https://s3-us-west-2.amazonaws.com/nu-yifeng/'
    # parser = argparse.ArgumentParser(description="Download data from S3")
    # # add argument
    # parser.add_argument("file_key", type=str,help="Name of the file in S3 that you want to download")
    # parser.add_argument("output_file_path", type=str,help="output path for downloaded file")

    # args = parser.parse_args()
    download_data(url,"lyrics.csv", '../data/lyrics.csv')