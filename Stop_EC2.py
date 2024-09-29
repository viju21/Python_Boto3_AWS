import boto3
from botocore.exceptions import ClientError

# Initialize EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Function to stop all running EC2 instances
def stop_all_ec2_instances():
    try:
        # Describe all instances with 'running' state
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )

        # Get the IDs of running instances
        running_instance_ids = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
        ]

        if running_instance_ids:
            # Stop the instances
            response = ec2_client.stop_instances(InstanceIds=running_instance_ids)
            print(f"Stopping Instances: {running_instance_ids}")
            for instance in response['StoppingInstances']:
                print(f"Instance {instance['InstanceId']} is {instance['CurrentState']['Name']}")
        else:
            print("No running instances found.")
    except ClientError as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    stop_all_ec2_instances()
