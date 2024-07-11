import boto3
from botocore.exceptions import ClientError

# Create ec2 client
ec2 = boto3.client('ec2')

# Create a new instance function
def create_instance(user_input):
    response = ec2.run_instances(
        ImageId="ami-0f76a278bc3380848", # TODO hardcoded value needs to be changed
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='WordpressDeham14',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
                'SubnetId': 'subnet-07e16952d8589584f', # TODO hardcoded value needs to be changed
                'Groups': ['sg-07053caff48096429'], # TODO hardcoded value needs to be changed
            },
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': user_input
                    },
                ]
            },
        ],
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f'Instance created with id: {instance_id}')

    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print('Instance is now running')

# Create function that terminates an instance
def terminate_instance(instance_id):
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f'Instance {instance_id} terminated successfully')
    except ClientError as e:
        print(f'Error: {e}')

# Function to list all instances
def list_instances():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_name = None
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break
            print(f'Instance Name: {instance_name}, Instance ID: {instance_id}, Status: {instance_state}')



