import os

#encryption decryption
key = ""
iv = ""
salt = ""

#aws credentials
aws_access_key = "aws_secret_key"
aws_secret_key = "aws_secret_key"
bucket_name = "spotify-etl-job"
s3_directory = "processed_data"

#spotify credentials
client_id = "client_id"
client_secret = "client_secret"
playlist_link = "https://open.spotify.com/playlist/4z5whwZPQuMotubMwwlsLB?si=qh_TRG2DTJu6QP8vg6dX6g"

#loca directory

raw_data = "/home/airflow/data/raw_data"
processed_data = "/home/airflow/data/processed_data"
