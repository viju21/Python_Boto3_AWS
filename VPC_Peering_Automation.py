#Author: VS
#Script_name: VPC_peering_automation.py
###Description: This script automates the acceptance of VPC peering requests. This is useful in hub-and-spoke network architectures where a central VPC initiates connections to multiple "spoke" VPCs. The script would:
    #1. Monitor for pending VPC peering requests.
    #2. Accept requests based on predefined criteria (e.g., specific tags, known requester VPC IDs).
    #3. Optionally, update route tables in both the requester and accepter VPCs to enable communication

import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2', region_name='us-east-1')

def create_vpc_peering_connection(requester_vpc_id, accepter_vpc_id):
    # Create a VPC Peering Connection
    response = ec2.create_vpc_peering_connection(
        VpcId=requester_vpc_id,
        PeerVpcId=accepter_vpc_id,
        PeerRegion='us-east-1'  # Update if your accepter VPC is in a different region
    )
    peering_connection_id = response['VpcPeeringConnection']['VpcPeeringConnectionId']
    print(f"Created VPC Peering Connection with ID: {peering_connection_id}")
    return peering_connection_id

def accept_vpc_peering_connection(peering_connection_id):
    # Accept the VPC Peering Connection
    response = ec2.accept_vpc_peering_connection(
        VpcPeeringConnectionId=peering_connection_id
    )
    print(f"Accepted VPC Peering Connection with ID: {peering_connection_id}")

def create_route(vpc_id, peering_connection_id, destination_cidr_block):
    # Create a route in the route table
    response = ec2.describe_route_tables(Filters=[
        {'Name': 'vpc-id', 'Values': [vpc_id]}
    ])
    route_table_id = response['RouteTables'][0]['RouteTableId']
    ec2.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock=destination_cidr_block,
        VpcPeeringConnectionId=peering_connection_id
    )
    print(f"Added route to Route Table {route_table_id} for {destination_cidr_block}")

def main():
    # Replace your Hub VPC ID and Spoke VPC ID
    hub_vpc_id = 'vpc-026b094f27b06e83f'
    spoke_vpc_id_1 = 'vpc-09bbfe3b1d6dcd167'
    spoke_vpc_id_2 = 'vpc-0ee9352f90ad82679'

    # Create VPC Peering Connections
    peering_connection_id_1 = create_vpc_peering_connection(hub_vpc_id, spoke_vpc_id_1)
    peering_connection_id_2 = create_vpc_peering_connection(hub_vpc_id, spoke_vpc_id_2)

    # Accept VPC Peering Connections
    accept_vpc_peering_connection(peering_connection_id_1)
    accept_vpc_peering_connection(peering_connection_id_2)

    # Create Routes
    create_route(hub_vpc_id, peering_connection_id_1, '10.1.0.0/16')
    create_route(hub_vpc_id, peering_connection_id_2, '10.2.0.0/16')
    create_route(spoke_vpc_id_1, peering_connection_id_1, '10.0.0.0/16')
    create_route(spoke_vpc_id_2, peering_connection_id_2, '10.0.0.0/16')

if __name__ == '__main__':
    main()






