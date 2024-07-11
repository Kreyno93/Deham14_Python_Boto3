import boto3

# Create VPC client
vpc = boto3.client('ec2')

# Create a new VPC function
def create_vpc(vpc_cidr):
    response = vpc.create_vpc(
        CidrBlock=vpc_cidr
    )

    vpc_id = response['Vpc']['VpcId']
    print(f'VPC created with id: {vpc_id}')

# Creates a new subnet function
def create_subnet(vpc_id, subnet_cidr):
    response = vpc.create_subnet(
        VpcId=vpc_id,
        CidrBlock=subnet_cidr
    )

    subnet_id = response['Subnet']['SubnetId']
    print(f'Subnet created with id: {subnet_id}')

# Function to list all VPCs
def list_vpcs():
    response = vpc.describe_vpcs()
    for vpc in response['Vpcs']:
        print(f'VPC id: {vpc["VpcId"]}')

# Function to list all subnets
def list_subnets():
    response = vpc.describe_subnets()
    for subnet in response['Subnets']:
        print(f'Subnet id: {subnet["SubnetId"]}')
