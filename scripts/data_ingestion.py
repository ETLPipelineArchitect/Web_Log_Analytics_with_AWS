import boto3

# Define your S3 bucket and log data location
s3_bucket = 'your-bucket'
s3_raw_path = 'web_server_logs/raw/'

# Function to upload logs to S3
def upload_logs_to_s3(file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, f'{s3_raw_path}{file_path}')

# Example usage
def main():
    upload_logs_to_s3('sample_logs.log')

if __name__ == '__main__':
    main()
