#author: Vijay Sankar C
#date: 10/07/2024
#description: This script is used to update the size of each prefix in a CSV file. 

#import section
import boto3
from botocore.exceptions import ClientError
from collections import defaultdict
import csv

#init client
s3_client = boto3.client('s3')

#def function for calculating prefix size
def calculate_prefix_size(bucket_name):
    try:
        prefix_size = defaultdict(int)
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get('Contents', []):
                key = obj['Key']
                size = obj['Size']
                prefix = key.split('/')[0] if '/' in key else key
                prefix_size[prefix] += size
        return dict(prefix_size)  # Convert defaultdict to dict before returning
    except ClientError as e:
        print(f"API Error Occurred: {e}")
        return {}  # Return an empty dictionary on API error
    except Exception as e:
        print(f"Error Occurred: {e}")
        return {}  # Return an empty dictionary on other errors

#def write function for writing into csv file
def write_csv(prefix_size, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Prefix', 'Size(bytes)'])
        for prefix, size in prefix_size.items():
            writer.writerow([prefix, size])

#def main function
def main():
    bucket_name = input("Enter the bucket name:").strip()
    output_file = 'prefix_sizes.csv'
    print(f"Calculating the prefix size of Bucket: {bucket_name}")
    prefix_size = calculate_prefix_size(bucket_name)
    if prefix_size:
        print(f"Writing the prefix size into CSV file: {output_file}")
        write_csv(prefix_size, output_file)
        print("CSV is written successfully.")
    else:
        print("No data to write.")

#main execution
if __name__ == '__main__':
    main()
