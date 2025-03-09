import os
import shutil
import logging
from typing import Optional
import config

logger = logging.getLogger(__name__)


class CleanupUtility:
    """Utility class for cleaning up local files and directories"""

    @staticmethod
    def delete_directory_contents(directory_path: str, remove_dir: bool = False) -> None:
        """Delete all contents of a directory, optionally remove the directory itself

        Args:
            directory_path (str): Path to directory to clean
            remove_dir (bool): Whether to remove the directory itself
        """
        try:
            if not os.path.exists(directory_path):
                logger.warning(f"Directory {directory_path} does not exist")
                return

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        logger.info(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        logger.info(f"Deleted directory: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}. Reason: {e}")

            if remove_dir:
                os.rmdir(directory_path)
                logger.info(f"Removed directory: {directory_path}")

        except Exception as e:
            logger.error(f"Error cleaning directory {directory_path}: {e}")
            raise

    @staticmethod
    def delete_specific_file(file_path: str) -> None:
        """Delete a specific file

        Args:
            file_path (str): Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
            else:
                logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise


def cleanup_after_processing(raw_data_path: Optional[str] = None):
    """Cleanup local files after processing and upload

    Args:
        raw_data_path (str, optional): Specific raw data file path to delete
    """
    try:
        # Clean processed data directories
        CleanupUtility.delete_directory_contents(config.processed_data, remove_dir=False)

        # Clean raw data directory
        if raw_data_path:
            CleanupUtility.delete_specific_file(raw_data_path)
        else:
            CleanupUtility.delete_directory_contents(config.raw_data, remove_dir=False)

        logger.info("Local data cleanup completed successfully")

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise
