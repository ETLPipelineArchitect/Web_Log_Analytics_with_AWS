import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, when, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder.appName("WebServerLogAnalysis").getOrCreate()

# Read Data from S3
target_s3_bucket = "s3://your-bucket/web_server_logs/raw/*.log"
logs_df = spark.read.text(target_s3_bucket)

# Define Regular Expression and Schema
log_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{{4}})\] "(.+?)" (\d{{3}}) (\S+) "(.*?)" "(.*?)"'
parsed_logs_df = logs_df.select(
    regexp_extract('value', log_pattern, 1).alias('host'),
    regexp_extract('value', log_pattern, 3).alias('user'),
    regexp_extract('value', log_pattern, 4).alias('timestamp'),
    regexp_extract('value', log_pattern, 6).cast(IntegerType()).alias('status')
)
# Additional Processing Steps here...

# Save Processed Data to S3
processed_data_path = "s3://your-bucket/web_server_logs/processed/data.parquet"
parsed_logs_df.write.parquet(processed_data_path, mode='overwrite')
