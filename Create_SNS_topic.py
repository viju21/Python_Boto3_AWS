#Author: VS
#Date: 2021-05-10
#Script_Name: Create_SNS_Topic.py
#Description: This script creates a SNS topic and subscribe an end-point to it on AWS.

import boto3
from botocore.exceptions import ClientError
#initialize client
sns_client = boto3.client('sns')

#def funct for creating an sns topic
def create_sns_topic(topic_name):
    try:
        response = sns_client.create_topic(Name= topic_name)
        topic_arn = response ['TopicArn']
        print(f"SNS topic of {topic_name} was created successfully. TopicArn:{topic_arn}.")
        return topic_arn
    except ClientError as e:
        print(f"Client Error has occured: {e}")
    except Exception as e:
        print(f"An Unknown error has occured:{e}")

#def funct for subscribing the topic
def subscribe_sns_topic(topic_arn, protocol, endpoint):
    try:
        if topic_arn is None:
            raise ValueError("The topic ARN provided is None. Ensure the topic was created successfully.")
        response = sns_client.subscribe(
            TopicArn = topic_arn,
            Protocol = protocol,
            Endpoint = endpoint
        )
        subscription_arn = response ['SubscriptionArn']
        print(f"Subscription to {endpoint} was successful. SubscriptionArn:{subscription_arn}")
    except ClientError as e:
        print(f"Client Error has occured: {e}")
    except Exception as e:
        print(f"An Unknown error has occured:{e}")

#call create sns topic  function 
topic_name = 'MySNSTopicForCWAlarm'
topic_arn = create_sns_topic(topic_name)

#call subscribe sns topic function
protocol = 'email'
endpoint = 'vijayviju900@gmail.com'
subscribe_sns_topic(topic_arn,protocol,endpoint)



