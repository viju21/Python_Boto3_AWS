import boto3
from botocore.exceptions import ClientError

# Initialize EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Function to create EC2 instance
def create_ec2_instance(instance_name, instance_type='t2.micro', ami_id='ami-00beae93a2d981137', key_name='Test_Boto3'):
        # Create EC2 instance
    try:
        response = ec2_client.run_instances(
            ImageId= 'ami-00beae93a2d981137',
            InstanceType='t2.micro',
            KeyName=key_name,
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': instance_name}
                    ]
                }
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance '{instance_name}' created with InstanceId: {instance_id}")
    
    except ClientError as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    instance_name = input("Enter the instance name: ")
    key_name = input("Enter the key pair name (without .pem): ")
    create_ec2_instance(instance_name, key_name=key_name)






