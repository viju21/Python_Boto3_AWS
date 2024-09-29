# Author: Vijay Sankar C
# Date: 10/07/24
# Description: This script should automate deletion of old, unused AMIs based on age or custom tags.

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants
AMI_RETENTION_PERIOD = 30
CUSTOM_TAG_KEY = "Delete"
CUSTOM_TAG_VALUE = "True"

# Initialize clients
ec2_client = boto3.client('ec2')

def delete_ami(ami_id):
    try:
        ec2_client.deregister_image(ImageId=ami_id)
        logging.info(f"Successfully De-registered AMI: {ami_id}")

        snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'description', 'Values': [f'*{ami_id}*']}])
        for snapshot in snapshots['Snapshots']:
            try:
                ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                logging.info(f"Successfully Deleted Snapshot: {snapshot['SnapshotId']}")
            except Exception as e:
                logging.error(f"Failed to delete Snapshot {snapshot['SnapshotId']} due to error: {e}")
    except ClientError as e:
        logging.error(f"Failed to delete AMI {ami_id} due to error: {e}")

def ami_verification(ami):
    try:
        creation_date = datetime.strptime(ami['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if creation_date < datetime.utcnow() - timedelta(days=AMI_RETENTION_PERIOD):
            logging.info(f"AMI {ami['ImageId']} is older than {AMI_RETENTION_PERIOD} days")
            return True
        if 'Tags' in ami:
            for tag in ami['Tags']:
                if tag['Key'] == CUSTOM_TAG_KEY and tag['Value'] == CUSTOM_TAG_VALUE:
                    return True
        return False
    except ClientError as e:
        logging.error(f"Failed to verify AMI {ami['ImageId']} due to error: {e}")
    except Exception as e:
        logging.error(f"Failed to verify AMI {ami['ImageId']} due to error: {e}")

def main():
    try:
        images = ec2_client.describe_images(Owners=['self'])
        for image in images['Images']:
            if ami_verification(image):
                logging.info(f"AMI {image['ImageId']} is marked for deletion")
                delete_ami(image['ImageId'])
            else:
                logging.info(f"AMI {image['ImageId']} is retained")
    except ClientError as e:
        logging.error(f"API Error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
