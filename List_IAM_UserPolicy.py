import boto3
from botocore.exceptions import ClientError

# Access AWS service using boto3
iam_client = boto3.client('iam')

# Define function for getting policies of a user
def list_attached_user_policies(user_name):
    try:
        response = iam_client.list_attached_user_policies(UserName=user_name)
        return response['AttachedPolicies']
    except ClientError as e:
        print(f"An error occurred: {e}")
        return []

# Main execution
if __name__ == "__main__":
    user_name = 'Test_Boto_AWS' #specify your user's username here
    # Get attached policies
    attached_policies = list_attached_user_policies(user_name)
    print("Attached Policies")
    for policy in attached_policies:
        print(f"PolicyName: {policy['PolicyName']}, PolicyARN: {policy['PolicyArn']}")
