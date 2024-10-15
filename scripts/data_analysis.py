from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("WebServerLogAnalysis").getOrCreate()

# Load Processed Data
processed_data_path = "s3://your-bucket/web_server_logs/processed/data.parquet"
data_df = spark.read.parquet(processed_data_path)

data_df.createOrReplaceTempView("web_logs")

# Perform Analytics Queries
# Example: Top 10 Most Requested Endpoints
most_requested = spark.sql("""
    SELECT endpoint, COUNT(*) as request_count
    FROM web_logs
    GROUP BY endpoint
    ORDER BY request_count DESC
    LIMIT 10
""")
most_requested.show()

# Save Output to S3
most_requested.write.csv("s3://your-bucket/web_server_logs/output/most_requested.csv", mode='overwrite')
