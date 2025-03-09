from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import config
from fetch_spotify_data import DataIngestion
from spotify_transformation import process_albums, process_artists, process_songs
from parquet_writer import ParquetWriter
from upload_to_s3 import UploadToS3
from s3_client_object import S3ClientProvider
from spark_session import spark_session
from cleanup_local_data import cleanup_after_processing

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        'spotify_etl_pipeline',
        default_args=default_args,
        description='ETL pipeline for Spotify data using Airflow',
        schedule_interval='@daily',
        catchup=False
) as dag:
    def fetch_data(**kwargs):
        """
        Fetch Spotify playlist data and save it locally.
        Returns the path to the saved JSON file.
        """
        logging.info("Starting Spotify data ingestion")
        di = DataIngestion(client_id=config.client_id, client_secret=config.client_secret)
        file_path = di.fetch_and_save_playlist_tracks(
            playlist_link=config.playlist_link,
            raw_data=config.raw_data
        )
        logging.info(f"Fetched data file at {file_path}")
        return file_path


    def transform_data(**kwargs):
        """
        Read the JSON file, transform the data with Spark, and write parquet files.
        """
        ti = kwargs['ti']
        file_path = ti.xcom_pull(task_ids='fetch_data')
        logging.info(f"Transforming data from file: {file_path}")

        # Initialize Spark session
        spark = spark_session()

        # Read JSON file into a Spark DataFrame using multiline option
        df_raw = spark.read.option("multiline", "true").json(file_path)

        # Process transformations
        df_albums = process_albums(df_raw)
        df_artists = process_artists(df_raw)
        df_songs = process_songs(df_raw)

        # Write processed data to parquet files in separate subfolders
        writer = ParquetWriter(mode="overwrite", data_format="parquet")
        writer.dataframe_writer(df_albums, config.processed_data, "albums")
        writer.dataframe_writer(df_artists, config.processed_data, "artists")
        writer.dataframe_writer(df_songs, config.processed_data, "songs")
        logging.info("Data transformation and parquet file writing completed.")


    def upload_data(**kwargs):
        """
        Upload the processed parquet files from the local processed data directory to S3.
        """
        logging.info("Starting upload to S3")
        s3_client = S3ClientProvider(aws_access_key=config.aws_access_key,
                                     aws_secret_key=config.aws_secret_key).get_client()
        uploader = UploadToS3(s3_client)
        subfolders = ["albums", "artists", "songs"]
        all_uploaded = []
        for subfolder in subfolders:
            uploaded_files = uploader.upload_to_s3(
                s3_directory=config.s3_directory,
                s3_bucket=config.bucket_name,
                base_folder=config.processed_data,
                subfolder_name=subfolder
            )
            all_uploaded.extend(uploaded_files)
        logging.info(f"Uploaded files: {all_uploaded}")


    def cleanup_data(**kwargs):
        """
        Cleanup the local raw and processed data after the pipeline run.
        """
        ti = kwargs['ti']
        file_path = ti.xcom_pull(task_ids='fetch_data')
        logging.info("Starting cleanup of local data")
        cleanup_after_processing(raw_data_path=file_path)
        logging.info("Local data cleanup completed.")


    fetch_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True
    )

    upload_task = PythonOperator(
        task_id='upload_data',
        python_callable=upload_data,
        provide_context=True
    )

    cleanup_task = PythonOperator(
        task_id='cleanup_data',
        python_callable=cleanup_data,
        provide_context=True
    )

    fetch_task >> transform_task >> upload_task >> cleanup_task
