# author: Vijay Sankar C
# date: 10/07/2024
# description: This script should analyze versioned buckets to identify potential storage cost optimizations (e.g., deleting old versions, transitioning to Intelligent Tiering).

import boto3
from botocore.exceptions import ClientError 
from datetime import datetime, timedelta

# Initialize clients
s3_client = boto3.client('s3')

# Define constants
VERSION_RETENTION_DAYS = 30  # Number of days to retain old versions
TRANSITION_DAYS = 60  # Number of days before transitioning to intelligent tier 

# Function to list all the buckets
def list_buckets():
    try:
        response = s3_client.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except ClientError as e:
        print(f"API Error occurred: {e}")

# Bucket analyzer function
def bucket_analyzer(bucket_name):
    try:
        response = s3_client.list_object_versions(Bucket=bucket_name)
        versions = response.get('Versions', [])
        for version in versions:
            last_modified = version['LastModified']
            version_id = version['VersionId']
            key = version['Key']
            size = version['Size']

            if last_modified < datetime.now(tz=last_modified.tzinfo) - timedelta(days=VERSION_RETENTION_DAYS):
                print(f"Deleting version {version_id} of {key} in bucket {bucket_name}, last modified: {last_modified}")

            if last_modified < datetime.now(tz=last_modified.tzinfo) - timedelta(days=TRANSITION_DAYS):
                print(f"Consider transitioning {key} (Version ID: {version_id}) to intelligent tier, last modified: {last_modified}")

    except ClientError as e:
        print(f"API Error occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Main function
def main():
    buckets = list_buckets()
    if not buckets:
        print("No Buckets Found")
    for bucket in buckets:
        bucket_analyzer(bucket)

# Main execution
if __name__ == '__main__':
    main()
