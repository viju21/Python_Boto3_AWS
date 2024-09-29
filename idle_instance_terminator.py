import boto3
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants
IDLE_THRESHOLD_CPU = 5.0  # CPU utilization threshold to consider an instance as idle
IDLE_THRESHOLD_NETWORK = 1000  # Network utilization threshold to consider an instance as idle

# Initialize AWS clients
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

def evaluate_instance(instance_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    
    # Fetch CPU utilization
    cpu_response = cloudwatch.get_metric_statistics(
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ]
    )
    
    cpu_data = cpu_response['Datapoints']
    cpu_utilization = cpu_data[0]['Average'] if cpu_data else 0
    
    # Fetch network utilization
    network_response = cloudwatch.get_metric_statistics(
        MetricName='NetworkIn',
        Namespace='AWS/EC2',
        Statistics=['Sum'],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ]
    )
    
    network_data = network_response['Datapoints']
    network_utilization = network_data[0]['Sum'] if network_data else 0
    
    return cpu_utilization, network_utilization

def main():
    logging.info("Fetching the list of running instances...")
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            logging.info(f"Evaluating instance {instance_id} for utilization...")
            cpu_utilization, network_utilization = evaluate_instance(instance_id)
            
            logging.info(f"CPU Utilization: {cpu_utilization:.2f}%")
            logging.info(f"Network Utilization: {network_utilization:.2f} bytes")
            
            if cpu_utilization < IDLE_THRESHOLD_CPU and network_utilization < IDLE_THRESHOLD_NETWORK:
                logging.info(f"Instance {instance_id} has low utilization: CPU {cpu_utilization:.2f}%, Network {network_utilization:.2f} bytes")
                
                # Create snapshot for the instance's volumes
                volumes = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
                for volume in volumes['Volumes']:
                    volume_id = volume['VolumeId']
                    snapshot = ec2.create_snapshot(VolumeId=volume_id, Description=f"Snapshot of {volume_id} before termination")
                    logging.info(f"Snapshot created for volume {volume_id} of instance {instance_id} (Snapshot ID: {snapshot['SnapshotId']})")
                
                # Terminate the instance
                termination_response = ec2.terminate_instances(InstanceIds=[instance_id])
                logging.info(f"Termination response for instance {instance_id}: {termination_response}")
                
                # Ensure termination was requested
                if termination_response['TerminatingInstances'][0]['CurrentState']['Name'] == 'shutting-down':
                    logging.info(f"Instance {instance_id} is being terminated.")
                else:
                    logging.warning(f"Instance {instance_id} was not successfully terminated.")
            else:
                logging.info(f"Instance {instance_id} is adequately utilized: CPU {cpu_utilization:.2f}%, Network {network_utilization:.2f} bytes")

if __name__ == "__main__":
    main()
