import boto3

ec2_client= boto3.client('ec2', region_name='us-east-1')
#list all instances 
def list_all_instances():
    try:
        response = ec2_client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID:{instance['InstanceId']} State:{instance['State']['Name']}")
    except Exception as e:
        print(f"The error Occured as {e}")

#Call the function
list_all_instances()
