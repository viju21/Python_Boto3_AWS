#Author: Vijay Sankar C
#Date: 24/07/2024
#script_name: cost_aware_auto_scaling.py
#description:This is the script that analyzes historical resource utilization (EC2, RDS, etc.), combined with real-time metrics. It should recommend scaling actions and suggest the most cost-effective instance types, AZ deployments, and potential Reserved Instance purchases to match future load.

#import sec
import boto3
from datetime import datetime, timedelta

# Initialize boto3 clients
cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')

# Define functions to gather data
def get_historical_metrics(namespace, metric_name, dimensions, start_time, end_time):
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # Increased period to 1 hour to reduce the number of datapoints
            Statistics=['Average', 'Maximum']
        )
        return response['Datapoints']
    except Exception as e:
        print(f"Error Occured: {e}")

def get_real_time_metrics(namespace, metric_name, dimensions):
         #get real-time metrics of Ec2 from the last 10min 
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=10)
        return get_historical_metrics(namespace, metric_name, dimensions, start_time, end_time)
    except Exception as e:
        print(f"Error Occured: {e}")

def get_instance_pricing(instance_type, purchase_option):   #Can change those values as requirement
    pricing_data = {
        'on_demand': {'t3.micro': 0.0104, 't3.small': 0.0208, 't3.medium': 0.0416, 't3.large': 0.0832},
        'reserved': {'t3.micro': 0.0072, 't3.small': 0.0144, 't3.medium': 0.0288, 't3.large': 0.0576}
    }
    return pricing_data[purchase_option][instance_type]

def recommend_instance_type(current_utilization):  #give recommendations of instance_type based on cpu utilization
    try:                                            
        if current_utilization < 20:
            return 't3.micro'
        elif current_utilization < 40:
            return 't3.small'
        elif current_utilization < 60:
            return 't3.medium'
        else:
            return 't3.large'
    except Exception as e:
        print(f"Error Occured:{e}")

def recommend_reserved_instances(instance_type):   #recommend reserved or on-demand based on the workload
    try:
        ri_pricing = get_instance_pricing(instance_type, 'reserved')
        on_demand_pricing = get_instance_pricing(instance_type, 'on_demand')
        
        if ri_pricing < on_demand_pricing * 0.75:  # Arbitrary threshold for cost-effectiveness
            return f"Purchase Reserved Instances for {instance_type}"
        else:
            return "Stick with On-Demand Instances"
    except Exception as e:
        print(f"Error occurred:{e}")

def recommend_az_deployments(instance_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        availability_zones = [res['Instances'][0]['Placement']['AvailabilityZone'] for res in response['Reservations']]
    #logic to recommend spreading instances across AZs
    
        az_recommendations = {}
        for az in set(availability_zones):
            az_recommendations[az] = availability_zones.count(az)
        
        total_instances = sum(az_recommendations.values())
        recommended_azs = {az: total_instances // len(az_recommendations) for az in az_recommendations}
        
        for az in az_recommendations:
            if az_recommendations[az] > recommended_azs[az]:
                diff = az_recommendations[az] - recommended_azs[az]
                for target_az in az_recommendations:
                    if az_recommendations[target_az] < recommended_azs[target_az]:
                        move_count = min(diff, recommended_azs[target_az] - az_recommendations[target_az])
                        az_recommendations[az] -= move_count
                        az_recommendations[target_az] += move_count
                        if diff == 0:
                            break
        
        return az_recommendations
    except Exception as e:
        print(f"Error Occurred as {e}")
# Example usage
namespace = 'AWS/EC2'
metric_name = 'CPUUtilization' 
dimensions = [{'Name': 'InstanceId', 'Value': 'i-0b03a300c2b1882f3'}] # Update the Instance ID to your actual Instance ID

# Get historical metrics
start_time = datetime.utcnow() - timedelta(days=30)
end_time = datetime.utcnow()
historical_metrics = get_historical_metrics(namespace, metric_name, dimensions, start_time, end_time)

# Check if historical metrics data is available and gather cpu utilization
if historical_metrics:
    average_utilization = sum(dp['Average'] for dp in historical_metrics) / len(historical_metrics)
else:
    average_utilization = 0
    print("No historical metrics data available.")

# Get real-time metrics and gather cpu utilization
real_time_metrics = get_real_time_metrics(namespace, metric_name, dimensions)

# Check if real-time metrics data is available and gather current utilization
if real_time_metrics:
    current_utilization = sum(dp['Average'] for dp in real_time_metrics) / len(real_time_metrics)
else:
    current_utilization = 0
    print("No real-time metrics data available.")

# Analyze metrics and make recommendations
recommended_instance_type = recommend_instance_type(current_utilization)
reserved_instance_recommendation = recommend_reserved_instances(recommended_instance_type)
az_deployment_recommendation = recommend_az_deployments('i-0b03a300c2b1882f3')

print(f"Average Utilization: {average_utilization:.2f}%")
print(f"Current Utilization: {current_utilization:.2f}%")
print(f"Recommended Instance Type: {recommended_instance_type}")
print(f"Reserved Instance Recommendation: {reserved_instance_recommendation}")
print(f"AZ Deployment Recommendation: {az_deployment_recommendation}")
