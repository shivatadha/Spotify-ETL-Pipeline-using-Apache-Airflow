import os
import datetime
import traceback
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class UploadToS3:
    """Class to handle file uploads to AWS S3."""

    def __init__(self, s3_client):
        """Initialize with an S3 client.

        Args:
            s3_client: Boto3 S3 client instance
        """
        self.s3_client = s3_client

    def _upload_file(self, local_path, s3_bucket, s3_key):
        """Upload a single file to S3.

        Args:
            local_path (str): Local file path
            s3_bucket (str): S3 bucket name
            s3_key (str): S3 key (path in bucket)
        """
        self.s3_client.upload_file(local_path, s3_bucket, s3_key)

    def upload_to_s3(self, s3_directory, s3_bucket, base_folder, subfolder_name):
        """Upload files from a local directory to S3 in parallel.

        Args:
            s3_directory (str): Base directory in S3
            s3_bucket (str): S3 bucket name
            base_folder (str): Local base folder
            subfolder_name (str): Subfolder containing files to upload

        Returns:
            list: List of S3 keys for uploaded files

        Raises:
            Exception: If uploading fails
        """
        local_file_path = os.path.join(base_folder, subfolder_name)
        current_epoch = int(datetime.datetime.now().timestamp()) * 1000
        s3_prefix = os.path.join(s3_directory, subfolder_name, str(current_epoch))

        try:
            files_to_upload = [(os.path.join(root, file), os.path.join(s3_prefix, file))
                               for root, _, files in os.walk(local_file_path) for file in files]

            if not files_to_upload:
                logger.warning(f"No files found in {local_file_path}")
                return []

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self._upload_file, local_path, s3_bucket, s3_key)
                           for local_path, s3_key in files_to_upload]
                for future in futures:
                    future.result()  # Raise any exceptions from threads

            uploaded_files = [s3_key for _, s3_key in files_to_upload]
            logger.info(f"Data successfully uploaded to {s3_directory}: {len(uploaded_files)} files")
            return uploaded_files
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            traceback_message = traceback.format_exc()
            logger.error(traceback_message)
            raise
