import boto3
from botocore.exceptions import ClientError

# Specify the region and create a bucket
def create_bucket(bucket_name):
    s3 = boto3.client('s3', region_name='eu-north-1')
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-north-1'
            }
        )
        print("Bucket Created Successfully")
    except ClientError as e:
        print(f'Error: {e}')

# Give me a list of all Buckets in a specific region
def list_buckets():
    s3 = boto3.client('s3', region_name='eu-north-1')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f'Bucket Name: {bucket["Name"]}')

# Delete a bucket
def delete_bucket(bucket_name):
    s3 = boto3.client('s3', region_name='eu-north-1')
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print("Bucket Deleted Successfully")
    except ClientError as e:
        print(f'Error: {e}')

# Delete all objects in a bucket
def delete_all_objects(bucket_name):
    s3 = boto3.client('s3', region_name='eu-north-1')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response['Contents']:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print("All objects deleted successfully")
    except ClientError as e:
        print(f'Error: {e}')

# Asks the user if they want to create a bucket
response = input("Do you want to create a bucket? (yes/no): ").strip().lower()
if response in ['yes', 'y']:
    bucket_name = input("Enter the bucket name you want to create: ").strip()
    create_bucket(bucket_name)
else:
    print("You chose not to create a bucket")

# Asks me if i want to list all buckets in a region
list_buckets()

# Asks me if i want to delete a bucket. If yes, it deletes the bucket. If there are objects in the bucket, it asks if i want to delete them
response = input("Do you want to delete a bucket? (yes/no): ").strip().lower()
if response in ['yes', 'y']:
    bucket_name = input("Enter the bucket name you want to delete: ").strip()
    delete_bucket(bucket_name)
    response = input("Do you want to delete all objects in the bucket? And then delete the bucket? (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        delete_all_objects(bucket_name)
        delete_bucket(bucket_name)
else:
    print("You chose not to delete a bucket")

