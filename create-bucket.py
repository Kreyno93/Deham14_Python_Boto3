import boto3
from botocore.exceptions import ClientError

# Specify the region and create a bucket. If it fails, ask as long as the user wants to try again
def create_bucket(bucket_name):
    s3 = boto3.client('s3', region_name='eu-north-1')
    while True:
        try:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'eu-north-1'
                }
            )
            print("Bucket Created Successfully")
            break
        except ClientError as e:
            print(f'Error: {e}')
            response = input("Do you want to try again? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                bucket_name = input("Enter the bucket name you want to create: ").strip()
            else:
                print("You chose not to try again")
                break

# Give me a list of all Buckets in a specific region
def list_buckets():
    s3 = boto3.client('s3', region_name='eu-north-1')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f'Bucket Name: {bucket["Name"]}')

# Delete a bucket
def delete_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f'Bucket {bucket_name} deleted successfully')
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketNotEmpty':
            print(f'Error: The bucket {bucket_name} is not empty.')
            raise
        else:
            print(f'Error: {e}')
            raise

# Delete all objects in a bucket
def delete_all_objects(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.objects.all().delete()
        print(f'All objects in the bucket {bucket_name} have been deleted successfully')
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
response = input("Do you want to list all buckets in the region? (yes/no): ").strip().lower()
if response in ['yes', 'y']:
    list_buckets()
else:
    print("You chose not to list all buckets")

# Asks me if i want to delete a bucket. If yes, it asks me for the bucket name
# If it fails due to the bucket not being empty, it asks me if i want to delete all objects in the bucket
response = input("Do you want to delete a bucket? (yes/no): ").strip().lower()
if response in ['yes', 'y']:
    try: 
        bucket_name = input("Enter the bucket name you want to delete: ").strip()
        delete_bucket(bucket_name)
    except ClientError as e:
        print(f'Error: {e}')
        if "BucketNotEmpty" in str(e):
            response = input("Do you want to delete all objects in the bucket? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                delete_all_objects(bucket_name)
                response = input("Do you want to delete the bucket now? (yes/no): ").strip().lower()
                if response in ['yes', 'y']:
                    delete_bucket(bucket_name)
            else:
                print("You chose not to delete all objects in the bucket")
else:
    print("You chose not to delete a bucket")

    

