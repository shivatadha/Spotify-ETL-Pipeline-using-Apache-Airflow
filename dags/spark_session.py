import logging
import findspark
findspark.init()
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

def spark_session():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("Spotify_Etl") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY") \
        .getOrCreate()
    logger.info("spark session %s", spark)
    return spark
