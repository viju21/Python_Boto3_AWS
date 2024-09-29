import boto3
from botocore.exceptions import ClientError,NoCredentialsError

# Initialize the client
s3_client = boto3.client('s3', region_name='us-east-1')

# Define Create Bucket function 
def create_bucket(bucket_name):
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name
        )
        print(f"Bucket '{bucket_name}' created successfully")
        print("Response Metadata", response['ResponseMetadata'])
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and owned by you.")
        elif e.response['Error']['Code'] == 'BucketAlreadyExists':
            print(f"Bucket '{bucket_name}' already exists.")
        elif e.response['Error']['Code'] == 'AccessDenied':
            print(f"You don't have permission to create bucket '{bucket_name}'.")
        else:
            print(f"An error occurred: {e}")
    except NoCredentialsError as e:
        print("Please ensure you are proceeding with correct credentials !!!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main Execution
if __name__ == "__main__":
    bucket_name = input("Enter the Bucket name: ")
    create_bucket(bucket_name)
