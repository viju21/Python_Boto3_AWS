import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3', region_name='us-east-1')
#list all buckets
def list_all_buckets():
    try:
        response = s3_client.list_buckets()
        print("Existing Buckets:")
        for bucket in response['Buckets']:
            print(f"{bucket['Name']}")
    except Exception as e:
        print(f"Error occured while listing all the buckets:{e}")

list_all_buckets()