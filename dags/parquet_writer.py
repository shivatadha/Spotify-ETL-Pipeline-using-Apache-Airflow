import logging
import traceback
import os
logger = logging.getLogger(__name__)


class ParquetWriter:
    def __init__(self, mode, data_format):
        self.mode = mode
        self.data_format = data_format

    def dataframe_writer(self, df, base_folder, subfolder_name):

        file_path = f"{base_folder}/{subfolder_name}"

        try:
            df.write.format(self.data_format) \
                .option("header", "true") \
                .mode(self.mode) \
                .option("path", file_path) \
                .save()
            logger.info(f"Data written successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error writing the data to {file_path}: {str(e)}")
            traceback_message = traceback.format_exc()
            print(traceback_message)
            raise e
