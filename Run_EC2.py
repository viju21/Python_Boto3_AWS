import boto3
from botocore.exceptions import ClientError

# Initialize EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Function to start specified EC2 instances
def start_ec2_instances(instance_ids):
    try:
        response = ec2_client.start_instances(InstanceIds=instance_ids)
        print(f"Starting the Instances {instance_ids}.")
        for instance in response['StartingInstances']:
            print(f"Instance {instance['InstanceId']} is {instance['CurrentState']['Name']}")
    except ClientError as e:
        print(f"Error Occurred: {e}")

# Main execution
if __name__ == "__main__":
    instance_ids = ['i-0f90c9404ad574c2a','i-06db927d9012f927d','i-0766c2a05fea7ccc1','i-0eae51539e6ec4bb5']  # Replace with your instance IDs
    start_ec2_instances(instance_ids)
